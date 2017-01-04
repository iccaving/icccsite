from pelican import signals
import logging
import os
from .photoreel import photoreel


def isarchive(generator):
    for article in generator.articles:
        # article = content
        if 'PHOTO_LOCATION' in generator.settings.keys():
            archive_loc = os.path.join(generator.settings['PHOTO_LOCATION'], '')
        else:
            archive_loc = ''
        logging.debug("Photoarchive: checking article " + article.title)
        if 'photoarchive' in article.metadata.keys():
            if article.photoarchive == '':
                if 'type' in article.metadata.keys():
                    archive_loc = os.path.join(archive_loc, article.type + 's/')
                if 'location' in article.metadata.keys() and 'date' in article.metadata.keys():
                    archive_loc = os.path.join(archive_loc, article.date.strftime('%Y-%m-%d') + '%20-%20' + article.location + '/')
                article.metadata['archiveloc'] = archive_loc.lower()
                article.archiveloc = archive_loc.lower()
            else:
                article.metadata['archiveloc'] = os.path.join(article.photoarchive, '')
                article.archiveloc = os.path.join(article.photoarchive, '')

            link = article.archiveloc
            try:
                article.data["photolink"] = """<div class="photo-button-wrapper"><a class="photo-button" href='""" + link + """'>Photos</a></div>"""
            except:
                article.data = {}
                article.data["photolink"] = """<div class="photo-button-wrapper"><a class="photo-button" href='""" + link + """'>Photos</a></div>"""
            if 'mainimg' in article.metadata.keys():
                image = article.archiveloc + article.metadata['mainimg']
                try:
                    article.data["mainimg"] = """<div class='mainimg'><a href='""" + link + """'><img src='""" + image + """'></a></div>"""
                except:
                    article.data = {}
                    article.data["mainimg"] = """<div class='mainimg'><a href='""" + link + """'><img src='""" + image + """'></a></div>"""

def register():
    signals.article_generator_pretaxonomy.connect(isarchive)
    signals.article_generator_pretaxonomy.connect(photoreel)
