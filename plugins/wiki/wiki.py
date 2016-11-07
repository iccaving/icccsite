from pelican import signals, utils
from collections import namedtuple
import os
import re
import logging

Article = namedtuple('Article', 'metadata content')
Article_for_list = namedtuple('Article_for_list', 'level path article subdirs')


class dotdict(dict):

    """dot.notation access to dictionary attributes"""
    # Makes things a bit more readable
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def wiki_init(generator):
    generator.context['wikiarticles'] = []


def construct_dir_map(generator, root, path, indexarticle):
    readers = generator.readers
    # Set up dictionary partial to desribe this subdirectory
    # Index: the metadata and content that this subdirs index should have
    # Articles: list of the articles in this subdir
    # Children: List of directories in this subdir
    # Path: relative path to this subdir
    subdir = dotdict(
        {"index": None, "articles": [], "children": [], "path": None})
    # Get relative path
    subdir.path = os.path.join(path.replace(root, ""), "")

    # If an article has the same name as a directory (on the same directory
    # level) then the article's metadata and content will be userd for that
    # dir's index
    # The scope of the function means that it cannot 'see' the index article
    # as it is one dir level higher, so it must be provided as a parameter
    if indexarticle is not None:
        metadata = indexarticle.metadata
        content = indexarticle.content
    else:
        filepath = os.path.dirname(os.path.dirname(os.path.join(subdir.path)))
        content = ""
        metadata = {"title":  os.path.basename(
            os.path.normpath(path)), "type": "wiki", "filepath": filepath, "autogen": True}
        # Transform metadata dictionary into named tuple for dot notation access
        # to attributes in the template
        metadata = namedtuple('metadata', [x for x in metadata.keys()])(
            *[metadata[x] for x in metadata.keys()])

    # Set this subdirs index file data
    subdir.index = Article(metadata, content)

    # Get the articles in a dict (so they can be looked up in dir loop)
    articles = {}
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            # Use pelicans markdown parser to convert markdown -> html
            parsedfile = readers.read_file(path, item)
            metadata = parsedfile.metadata
            metadata["filepath"] = os.path.join(subdir.path, item)
            metadata = namedtuple('metadata', [x for x in metadata.keys()])(
                *[metadata[x] for x in metadata.keys()])
            content = parsedfile.content
            # Put in dictionary, key is filename without .md file extension
            articles[os.path.splitext(item)[0]] = Article(metadata, content)

    # Now go through the directories, matching up the 'index' articles, and
    # recursively calling this subdir parser
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            if item in articles:
                # If an article has the same name, pass it to the subdirectory
                # to be used as the index, then delete from this subdirs article
                # list
                subdir.children.append(
                    construct_dir_map(generator, root, os.path.join(path, item), articles[item]))
                del articles[item]
            else:
                subdir.children.append(
                    construct_dir_map(generator, root, os.path.join(path, item), None))
    # Convert articles from dict to list
    for article in articles:
        subdir.articles.append(articles[article])

    return subdir


def parse_wiki_pages(generator):
    settings = generator.settings
    readers = generator.readers
    contentpath = settings.get("PATH", "content")

    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/wiki")))

    # Begin with parsing main wiki page
    parsedfile = readers.read_file(root, "index.md")
    metadata = parsedfile.metadata
    metadata["filepath"] = ""
    metadata = namedtuple('metadata', [x for x in metadata.keys()])(
        *[metadata[x] for x in metadata.keys()])
    content = parsedfile.content

    # Contruct dictionary representation of folder structure
    wiki = construct_dir_map(generator, root, root, Article(metadata, content))

    generator.context['wiki'] = wiki
    logging.debug("Wiki: Wiki assembled")


def wiki_dic_to_list(wiki, level):
    wiki_list = []
    wiki_list_articles = []
    sub_wiki_list = []
    sub_wiki_list_articles = []

    # Construct a 'sub-list' of all items below in and below this sub directory
    # to be available to this dirs index page, with the 'levels' reletive to
    # this dir

    for subdir in sorted(wiki.children, key=lambda child: child.path):
        sub_wiki_list = sub_wiki_list + wiki_dic_to_list(subdir, 0)

    for article in wiki.articles:
        article_list_item = Article_for_list(
            0, wiki.path + article.metadata.title + ".html", article, None)
        sub_wiki_list_articles.append(article_list_item)

    sub_wiki_list_articles = sorted(sub_wiki_list_articles, key=lambda art: art.article.metadata.title)
    sub_wiki_list = sub_wiki_list + sub_wiki_list_articles

    # URLs look nicer without the index.html I think (but they need to be in for
    # the pelican write to write the file)
    for i, item in enumerate(sub_wiki_list):
        if "index.html" in item.path:
            sub_wiki_list[i] = item._replace(
                path=item.path.replace("index.html", ""))

    index_list_item = Article_for_list(
        level, wiki.path + "index.html", wiki.index, sub_wiki_list)
    wiki_list.append(index_list_item)

    # Contruct a sub list to be passed back up, with 'levels' relativer to
    # whatever dir is asking for them
    for subdir in sorted(wiki.children, key=lambda child: child.path):
        wiki_list = wiki_list + wiki_dic_to_list(subdir, level + 1)

    for article in wiki.articles:
        article_list_item = Article_for_list(
            level + 1, wiki.path + article.metadata.title + ".html", article, None)
        wiki_list_articles.append(article_list_item)

    wiki_list_articles = sorted(wiki_list_articles, key=lambda art: art.article.metadata.title)
    wiki_list = wiki_list + wiki_list_articles

    return wiki_list


def generate_wiki_pages(generator, writer):
    wiki = generator.context['wiki']

    # Get a flat list of wiki articles for easy use in a template
    wiki_list = wiki_dic_to_list(wiki, 0)

    # Write the pages!
    template = generator.get_template('wikiarticle')
    for page in wiki_list:
        filename = 'wiki' + page.article.metadata.filepath.replace('.md', '.html')
        content = page.article.content
        content = re.sub(r'\.md', '.html', content)
        metadata = page.article.metadata
        subdirs = page.subdirs
        path = page.path
        writer.write_file(filename, template, generator.context,
                          meta=metadata, content=content, subdirs=subdirs, path=path)



def register():
    # Registers the various functions to run during particar Pelican processes
    signals.article_generator_init.connect(wiki_init)
    # Run after the article list has been generated
    signals.article_generator_finalized.connect(parse_wiki_pages)
    # Run after the articles have been written
    signals.article_writer_finalized.connect(generate_wiki_pages)
