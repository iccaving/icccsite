from pelican import signals, utils
from collections import namedtuple
import os
import re
import logging
import pprint

pp = pprint.PrettyPrinter(indent=4)

"""
Article = namedtuple('Article', 'metadata content')
Article_for_list = namedtuple('Article_for_list', 'level path article subdirs')


class dotdict(dict):

    # dot.notation access to dictionary attributes
    # Makes things a bit more readable
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

"""

#def wiki_init(generator):

def add_to_structure(structure, path_list):
    folders = structure["folders"]
    articles = structure["articles"]
    dir = path_list[0]
    rest = path_list[1:]

    if len(rest) > 1:
        if dir in folders:
            folders[dir] = add_to_structure(folders[dir], rest)
        else:
            folders[dir] = add_to_structure({"folders":{},"articles":[]}, rest)
    else:
       if dir in folders:
           folders[dir]["articles"].append(rest)
       else:
           folders[dir] = { "folders": {}, "articles": [ rest ] }
    
    return { "folders": folders, "articles": articles }

def parse_wiki_pages(generator):
    settings = generator.settings
    readers = generator.readers
    contentpath = settings.get("PATH", "content")

    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath, "wiki", "")))

    list = []
    structure = {"folders":{}, "articles":[]}

    for (dirname, dirnames, filenames) in os.walk(root):
        for file in filenames:
            if ".git" not in dirname and ".git" not in file:
                parsedfile = readers.read_file(dirname, file)
                metadata = parsedfile.metadata
                org = metadata["path"].split("/")
                org.append(file)
                structure = add_to_structure(structure, org)
                list.append((metadata["path"],file,parsedfile))
                
    structure = { "articles": structure["folders"]['']["articles"], "folders":structure["folders"] }
    del(structure["folders"][""])
    list.sort()
    generator.context['wikilist'] = list
    generator.context['wiki'] = structure
    #logging.debug("Wiki: Wiki assembled")


def parse_dict(structure, path, level, nice_list):
    folders = {}
    for key in sorted(structure["folders"].keys()):
        print(key)
        folders[key] = structure["folders"][key]
    articles = structure["articles"]
    for key in folders.keys():
        nice_list.append((key, path, level))
        nice_list = parse_dict(folders[key], os.path.join(path, key), level + 1, nice_list)
    for item in articles:
        item = item[0]
        nice_list.append((item, path, level))
    return nice_list

def generate_wiki_pages(generator, writer):
    wiki_list = generator.context['wikilist']
    structure = generator.context['wiki']
    template = generator.get_template('wikiarticle')
    nice_list = parse_dict(structure, "wiki" , 0, [])

    for page in wiki_list:
        filename = os.path.join('wiki',  page[1].replace('.md', '.html'))
        content = page[2].content
        metadata = page[2].metadata
        path = page[0]
        file = page[1]
        writer.write_file(filename, template, generator.context,
                          meta=metadata, content=content, file=file, path=path, links=nice_list)


def register():
    # Registers the various functions to run during particar Pelican processes
    #signals.article_generator_init.connect(wiki_init)
    # Run after the article list has been generated
    signals.article_generator_finalized.connect(parse_wiki_pages)
    # Run after the articles have been written
    signals.article_writer_finalized.connect(generate_wiki_pages)
