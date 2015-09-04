from pelican import signals, utils
from collections import namedtuple, defaultdict, OrderedDict
import os
import logging


def getoldurl(generator):
    oldurls = []
    for article in generator.articles:  # Loop through articles
        # If the article has the oldurl metadata
        if 'oldurl' in article.metadata.keys():
            oldurls.append(
                (article.metadata['oldurl'], generator.settings["SITEURL"] + "/" + article.url))
    generator.context['oldurls'] = oldurls


def generatehtaccess(generator, writer):
    oldurls = generator.context['oldurls']
    template = generator.get_template('htaccess')
    filename = '.htaccess'
    writer.write_file(filename, template, generator.context, oldurls=oldurls)


def register():
    # Registers the various functions to run during particar Pelican processes
    # Run after the article list has been generated
    signals.article_generator_finalized.connect(getoldurl)
    # Run after the articles have been written
    signals.article_writer_finalized.connect(generatehtaccess)
