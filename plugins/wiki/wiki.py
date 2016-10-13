from pelican import signals, utils
from collections import namedtuple, defaultdict, OrderedDict
import os
from datetime import date, datetime
import logging
import string
import sys
import re
import copy

def wikiinit(generator):
    generator.context['wikiarticles'] = []

def parsewikipages(generator):
    settings = generator.settings
    readers = generator.readers
    contentpath = settings.get("PATH", "content")
    # There are files descirbing people/caves in the cave/caver directories
    # Look through cave/caver directory and process the markdown files therein
    # The outputted html is then saved along with the filename in a dictionary
    # which is added to the global context
    # The filename should match a name used in trip reports
    wikis = {}
    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/wiki")))
    for dirpath, dirnames, filenames in os.walk(root):
        for afile in filenames:
            parsedfile = readers.read_file(dirpath, afile)
            content = parsedfile.content
            metadata = parsedfile.metadata
            # Create a tuple of the bio content and any metadata.
            # The metadata is made into a named tuple so its nicer
            # to access the items in it from the template
            wikis[os.path.splitext(afile)[0]] = (content, namedtuple(
                'metadata', [x for x in metadata.keys()])(*[metadata[x] for x in metadata.keys()]))

    generator.context['wikiarticles'] = wikis
    logging.debug("Wiki: Wiki assembled")

def generatewikipages(generator, writer):
    # For each person generate a page listing the caves they have been in and the article that
    # describes that trip
    wiki = generator.context['wikiarticles']

    template = generator.get_template('wikiarticle')
    for article in wiki:
        filename = 'wiki/' + article + '.html'
        articlecontent = wiki[article][0]
        metadata = wiki[article][1]
        writer.write_file(filename, template, generator.context, meta=metadata, content=articlecontent)

    # ==========Write the index of cavers================

    template = generator.get_template('wikiindex')
    filename = 'wiki/index.html'
    writer.write_file(filename, template, generator.context, articles=wiki)

def register():
    # Registers the various functions to run during particar Pelican processes
    signals.article_generator_init.connect(wikiinit)
    # Run after the article list has been generated
    signals.article_generator_finalized.connect(parsewikipages)
    # Run after the articles have been written
    signals.article_writer_finalized.connect(generatewikipages)
