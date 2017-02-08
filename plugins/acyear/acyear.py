from pelican import signals
from collections import namedtuple
import logging

# This plugin is intended to enable populating the sidebar with trips sorted by
# academic year
def articles_by_academic_year(generator):
    # Create a list of article objects and their associated academic year
    generator.context['trips_by_academic_year'] = []
    row = namedtuple('row', 'date academic_year article')
    for article in generator.context['articles']:
        if 'type' in article.metadata.keys():
            # Only do this if the article is a trip because it only matters for the sidebar
            # ordering
            if article.type == 'trip':
                # The boundary is august/september
                if int(article.date.strftime('%m')) > 8:
                    year1 = article.date.strftime('%Y')
                    year2 = str(int(article.date.strftime('%Y')) + 1)
                else:
                    year1 = str(int(article.date.strftime('%Y')) - 1)
                    year2 = article.date.strftime('%Y')
                generator.context['trips_by_academic_year'].append(row(article.date, year1 + '-' + year2, article))


def register():
    # After each article is processed add it to the acyear list
    signals.article_generator_finalized.connect(articles_by_academic_year)
