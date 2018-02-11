import os
from datetime import datetime
from olm.article import Article
from photoreel import photoreel


def isarchive(sender, context, article):
    if 'PHOTO_LOCATION' in context:
        archive_loc = os.path.join(context['PHOTO_LOCATION'], '')
    else:
        archive_loc = ''
    #logger.debug("Photoarchive: checking article " + article.title)

    if 'photoarchive' in article.metadata:
        if article.metadata['photoarchive'] == '':
            if 'type' in article.metadata:
                archive_loc = os.path.join(archive_loc, article.type + 's/')
            if 'location' in article.metadata and 'date' in article.metadata:
                archive_loc = os.path.join(archive_loc, article.date.strftime('%Y-%m-%d') + '%20-%20' + article.location + '/')
            article.metadata['archiveloc'] = archive_loc.lower()
            #article.archiveloc = archive_loc.lower()
        else:
            article.metadata['archiveloc'] = os.path.join(article.metadata['photoarchive'], '')
            #article.archiveloc = os.path.join(article.photoarchive, '')

        link = article.metadata['archiveloc']
        try:
            article.data["photolink"] = """<div class="photo-button-wrapper"><a class="photo-button" href='""" + link + """'>Photos</a></div>"""
        except:
            article.data = {}
            article.data["photolink"] = """<div class="photo-button-wrapper"><a class="photo-button" href='""" + link + """'>Photos</a></div>"""
        if 'mainimg' in article.metadata:
            image = article.metadata['archiveloc'] + article.metadata['mainimg']
            try:
                article.data["mainimg"] = """<div class='mainimg'><a href='""" + link + """'><img src='""" + image + """'></a></div>"""
            except:
                article.data = {}
                article.data["mainimg"] = """<div class='mainimg'><a href='""" + link + """'><img src='""" + image + """'></a></div>"""

def register():
    return [
        ("AFTER_ARTICLE_READ", isarchive),
        ("AFTER_ALL_ARTICLES_READ", photoreel)
    ]
    
