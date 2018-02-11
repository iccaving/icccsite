from collections import namedtuple

# This plugin is intended to enable populating the sidebar with trips sorted by
# academic year
def articles_by_academic_year(sender, context, articles):
    # Create a list of article objects and their associated academic year
    context['trips_by_academic_year'] = []
    row = namedtuple('row', 'date academic_year article')
    for article in sorted(articles, key=lambda k: (k.date), reverse=True):
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
                context['trips_by_academic_year'].append(row(article.date, year1 + '-' + year2, article))


def register():
    return ("AFTER_ALL_ARTICLES_READ", articles_by_academic_year)
