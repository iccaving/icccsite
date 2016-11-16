from collections import namedtuple
from pelican.contents import Article
from pelican import signals
import os
import logging
import re
import copy

def create_or_add(dictionary, key_to_add, data_to_add):
    if key_to_add in dictionary:
        dictionary[key_to_add] = dictionary[key_to_add] + data_to_add
    else:
        dictionary[key_to_add] = data_to_add

def construct_bios(generator):
    settings=generator.settings
    readers=generator.readers
    contentpath=os.path.realpath(os.path.abspath(settings.get("PATH", "content")))
    logging.debug("Cavebios: Cavebios starting")

    def get_bios(path):
        dictionary = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for afile in filenames:
                logging.debug("Cavebios: Reading {}/{}".format(dirpath, afile))
                article = readers.read_file(
                            base_path=dirpath,
                            path=afile,
                            content_class=Article,
                            context=generator.context)
                dictionary[os.path.splitext(afile)[0]]=article
        return dictionary

    generator.context['caverbios']= get_bios(os.path.join(contentpath, "cavers"))
    logging.debug("Cavepeep: Caver bios assembled")

    generator.context['cavebios'] = get_bios(os.path.join(contentpath, "caves"))
    logging.debug("Cavepeep: Cave bios assembled")

def get_data_from_metadata(metadata):
    data = {}
    for key in metadata.keys():
        if key == "location":
             data["map"] = """<div class="padmore"><iframe width="100%" height="450" frameborder="0" style="border:0" allowfullscreen src="https://www.google.com/maps/embed/v1/search?q=""" + re.sub(r',\s*', "%2C", metadata["location"].strip()) + """&maptype=satellite&key=AIzaSyB03Nzox4roDjtKoddF9xFcYsvm4vi26ig" allowfullscreen></iframe></div>"""
    return data

def generate_cave_pages(generator, writer):
    cave_bios=generator.context['cavebios']
    caves = generator.context['cavepeep_cave']
    caves_dict = {}

    # Split the through trips into individual caves.
    # Make unique list (set) of cave names and
    for trip in caves:
        for cave in trip.split('>'):
            create_or_add(caves_dict, cave.strip(), caves[trip])

    dictionary = caves_dict
    content_dictionary = cave_bios
    output_path = "caves"
    template = "cavepages"


    row = namedtuple('row', 'path content metadata articles')
    initialised_pages = {}

    for key in dictionary.keys():
        if key not in initialised_pages.keys():
            logging.debug("Cavebios: Adding {} to list of pages to write".format(key))
            content=''
            metadata=''
            data={}
            if key in content_dictionary:
                logging.debug("Cavebios: Content added to " + key)
                content = content_dictionary[key].content
                metadata = content_dictionary[key].metadata
                metadata['data'] = get_data_from_metadata(metadata)

            path= os.path.join(output_path, str(key) + '.html')
            initialised_pages[key]=(row(path, content, metadata, dictionary[key]))
        else:
            initialised_pages[key].articles.extend(dictionary[key])

    for page_name, page_data in initialised_pages.items():
        #logging.debug("Cavebios: Writing {}".format(page_name))
        article = Article(page_data.content, page_data.metadata)
        writer.write_file(  page_data.path,
                            template = generator.get_template(template),
                            context = generator.context,
                            pagename=page_name,
                            articles=sorted(page_data.articles, key=lambda x: x.date, reverse=True),
                            article=article)

    # ==========Write the index of caves================
    pages = initialised_pages
    row=namedtuple('row', 'name number recentdate meta')
    rows = []
    for page_name in pages.keys():
        name = page_name;
        number = len(pages[page_name].articles)
        recentdate = max([article.date for article in pages[page_name].articles])
        meta = content_dictionary[page_name].metadata if page_name in content_dictionary.keys() else None
        rows.append(row(name, number, recentdate, meta))
    filename=os.path.join(output_path, 'index.html')
    writer.write_file(  filename,
                        template = generator.get_template(template + "_index"),
                        context = generator.context,
                        rows=sorted(rows, key=lambda x: x.name))

def generate_person_pages(generator, writer):
    # For each person generate a page listing the caves they have been in and the article that
    # describes that trip
    author_list={}
    caver_bios=generator.context['caverbios']
    cavers=generator.context['cavepeep_person']

    dictionary = cavers
    content_dictionary = caver_bios
    output_path = "cavers"
    template = "caverpages"

    for item in generator.authors:
        author_list[item[0].name]=item[1]

    row = namedtuple('row', 'path content metadata articles authored')
    initialised_pages = {}

    for key in dictionary.keys():
        if key not in initialised_pages.keys():
            logging.debug("Cavebios: Adding {} to list of pages to write".format(key))
            content=''
            metadata=''
            authored=[]
            #print(key)
            #print(author_list.keys())
            if key in author_list.keys():
                authored = author_list[key]
            path= os.path.join(output_path, str(key) + '.html')
            initialised_pages[key]=(row(path, content, metadata, dictionary[key], authored))
        else:
            initialised_pages[key].articles.extend(dictionary[key])

    for page_name, page_data in initialised_pages.items():
        #logging.debug("Cavebios: Writing {}".format(page_name))
        article = Article(page_data.content, page_data.metadata)
        writer.write_file(  page_data.path,
                            template = generator.get_template(template),
                            context = generator.context,
                            personname=page_name,
                            articles=sorted(page_data.articles, key=lambda x: x.date, reverse=True),
                            article=article,
                            authored=page_data.authored)
    pages = initialised_pages
    # ==========Write the index of cavers================
    row=namedtuple('row', 'name number recentdate meta')
    rows = []
    for page_name in pages.keys():
        name = page_name;
        number = len(pages[page_name].articles)
        recentdate = max([article.date for article in pages[page_name].articles])
        meta = content_dictionary[page_name].metadata if page_name in content_dictionary.keys() else None
        rows.append(row(name, number, recentdate, meta))
    filename=os.path.join(output_path, 'index.html')
    writer.write_file(  filename,
                        template = generator.get_template(template + "_index"),
                        context = generator.context,
                        rows=sorted(sorted(rows, key=lambda x: x.name), key=lambda x: x.recentdate, reverse=True))
