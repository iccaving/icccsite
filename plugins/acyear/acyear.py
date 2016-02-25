from pelican import signals
from collections import namedtuple
import logging

# This plugin is intended to enable populating the sidebar with trips sorted by
# academic year


def acyear(generator):
    # Create a list of article objects and their associated academic year
    yearlist = []
    row = namedtuple('row', 'date acyear article')
    for article in generator.articles:
        if 'type' in article.metadata.keys():
            # Only do this if the article is a trip because it only matters for the sidebar
            # ordering
            if article.type == 'trip' and 'unlisted' not in article.metadata.keys():
                # The boundary is august/september
                if int(article.date.strftime('%m')) > 8:
                    year1 = article.date.strftime('%Y')
                    year2 = str(int(article.date.strftime('%Y')) + 1)
                    yearlist.append(
                        row(article.date, year1 + '-' + year2, article))
                else:
                    year1 = str(int(article.date.strftime('%Y')) - 1)
                    year2 = article.date.strftime('%Y')
                    yearlist.append(
                        row(article.date, year1 + '-' + year2, article))

    # Sort the list by date (the full date, not academic year) and make
    # available to generator context (so the templates can access it)
    generator.context['yearlist'] = sorted(
        yearlist, key=lambda x: x.date, reverse=True)
    logging.debug("acyear: Success!")


def register():
    # After the list of articles has been generated, do acyear
    signals.article_generator_finalized.connect(acyear)
