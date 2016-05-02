from pelican import signals
from collections import namedtuple
import logging

# This plugin is intended to enable populating the sidebar with trips sorted by
# academic year

def acyearinit(generator):
    generator.context['yearlist'] = []

def acyear(generator, content):
    # Create a list of article objects and their associated academic year
    article = content
    row = namedtuple('row', 'date acyear article')
    if 'type' in article.metadata.keys():
        # Only do this if the article is a trip because it only matters for the sidebar
        # ordering
        if article.type == 'trip' and 'unlisted' not in article.metadata.keys():
            # The boundary is august/september
            if int(article.date.strftime('%m')) > 8:
                year1 = article.date.strftime('%Y')
                year2 = str(int(article.date.strftime('%Y')) + 1)
                generator.context['yearlist'].append(
                    row(article.date, year1 + '-' + year2, article))
            else:
                year1 = str(int(article.date.strftime('%Y')) - 1)
                year2 = article.date.strftime('%Y')
                generator.context['yearlist'].append(
                    row(article.date, year1 + '-' + year2, article))


def register():
    #Set up the acyear list
    signals.article_generator_init.connect(acyearinit)
    # After each article is processed add it to the acyear list
    signals.article_generator_write_article.connect(acyear)
