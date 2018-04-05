from collections import namedtuple, OrderedDict
import os
import re
import codecs
import time
from olm.helper import Map
from olm.reader import Reader
from olm.source import Source
from olm.logger import get_logger
from olm.writer import Writer

logger = get_logger('olm.plugins.wiki')

def add_to_structure(structure, path_list):
    folders = structure["folders"]
    articles = structure["articles"]
    subdir = path_list[0]
    rest = path_list[1:]

    if len(rest) > 1:
        if subdir in folders:
            folders[subdir] = add_to_structure(folders[subdir], rest)
        else:
            folders[subdir] = add_to_structure({"folders":{},"articles":[]}, rest)
    else:
       if subdir in folders:
           folders[subdir]["articles"] += rest
       else:
           folders[subdir] = { "folders": {}, "articles": rest }
    
    return { "folders": folders, "articles": articles }

def parse_wiki_pages(sender, context, articles):
    time_start = time.time()
    contentpath = context.SOURCE_FOLDER

    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath, "wiki", "")))

    all_files = []
    wikilist = []
    structure = {"folders":{}, "articles":[]}
    for (dirname, dirnames, filenames) in os.walk(root):
        for filename in filenames:
            if ".git" not in dirname and ".git" not in filename:
                with codecs.open(os.path.join(dirname, filename), 'r', encoding='utf8') as md_file:
                    reader = Reader(md_file.read())
                    metadata, raw_content = reader.parse()
                basename, ext = os.path.splitext(filename)
                content = context.MD(raw_content)
                wikiarticle = Source(context, metadata=metadata, content=content, basename=basename)
                wikiarticle.cache_id = basename
                wikiarticle.cache_type = 'WIKI'
                try:
                    path = metadata["path"]
                    org = metadata["path"].split("/")
                except KeyError:
                    path = ""
                    org = []
                org.append(filename)
                structure = add_to_structure(structure, org)
                wikilist.append((path,filename,wikiarticle))
                all_files.append(wikiarticle)
                
    structure = { "articles": structure["folders"]['']["articles"], "folders":structure["folders"] }

    del(structure["folders"][""])
    wikilist.sort()
    context['wikilist'] = wikilist
    context['wiki'] = structure
    context['all_files'].extend(all_files)
    logger.info("Processed wiki in %.3f seconds", time.time() - time_start)


def parse_dict(structure, level, nice_list):
    folders = OrderedDict(sorted(structure["folders"].items(), key=lambda t: t[0]))
    articles = sorted(structure["articles"])
    for key in folders.keys():
        if key + ".md" in articles:
            nice_list.append((key, "indexdir", level))
            articles.remove(key + ".md")
        else:
            nice_list.append((key, "noindexdir", level))
        nice_list = parse_dict(folders[key], level + 1, nice_list)
    for item in articles:
        nice_list.append((item, "article", level))
    return nice_list

def generate_wiki_pages(sender, context):
    time_start = time.time()
    wiki_list = context['wikilist']
    structure = context['wiki']
    nice_list = parse_dict(structure, 0, [])

    number_written = 0
    for page in wiki_list:  
        same_as_cache = page[2].same_as_cache
        if same_as_cache:
            continue
        number_written = number_written + 1
        filename = os.path.join('wiki', page[1].replace('.md', '.html'))
        content = page[2].content
        metadata = page[2].metadata
        path = page[0]
        breadcrumbs = []
        for name in path.split('/'):
            name_match = [item[1] for item in nice_list if item[0] == name]
            if len(name_match) > 0 and name_match[0] == "indexdir":
                breadcrumbs.append((name, "a"))
            else:
                breadcrumbs.append((name, "p"))
        file = page[1]
        writer = Writer(
            context, 
            filename, 
            "wikiarticle.html",
            meta=metadata, 
            content=content, 
            file=file, 
            path=path, 
            links=nice_list, 
            breadcrumbs=breadcrumbs)
        writer.write_file()
    logger.info("Wrote %d changed wiki pages out of %d wiki pages in %.3f seconds", number_written, len(wiki_list), time.time() - time_start)

def register():
    return [
        ("BEFORE_CACHING", parse_wiki_pages),
        ("AFTER_WRITING", generate_wiki_pages)
    ]