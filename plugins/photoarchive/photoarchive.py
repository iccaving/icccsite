from pelican import signals
import logging
import os

def isarchive(generator):
    archives = []
    for article in generator.articles:
        if 'ROOTLOC' in generator.settings.keys():
            archive_loc = os.path.join(generator.settings['ROOTLOC'], '')
        else:
            archive_loc = ''
        logging.debug("Photoarchive: checking article " + article.title)
        if 'photoarchive' in article.metadata.keys():
            if article.photoarchive == '':
                archive_loc = '/rcc/caving/photo_archive/'
                if 'type' in article.metadata.keys():
                    archive_loc += article.type + 's/'
                if 'location' in article.metadata.keys() and 'date' in article.metadata.keys():
                    archive_loc += article.date.strftime('%Y-%m-%d') + '%20-%20' + article.location + '/'
                article.metadata['archiveloc'] = archive_loc.lower()
                article.archiveloc = archive_loc.lower()
            else:
                if article.photoarchive[0] == '/':
                    article.metadata['archiveloc'] = archive_loc + os.path.join(article.photoarchive, '')
                    article.archiveloc = archive_loc + os.path.join(article.photoarchive, '')
                else:
                    article.metadata['archiveloc'] = os.path.join(article.photoarchive, '')
                    article.archiveloc = os.path.join(article.photoarchive, '')

            archives.append((article.archiveloc, article.title, article.date.strftime('%d-%m-%Y')))

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
    generator.context['photoarchives'] = archives


def archivemaker(generator, writer):
    template = generator.get_template('photoindex')
    filename = "photo_archive/index_template.php"
    writer.write_file(filename, template, generator.context)
    logging.debug("Photoarchive: Generic photo archive page generated")


def photoarchivelist(generator, writer):
    template = generator.get_template('photoarchivelist')
    filename = "photo_archive/index.html"
    writer.write_file(filename, template, generator.context)
    logging.debug("Photoarchive: Photo archive list page generated")



def register():
    signals.article_generator_finalized.connect(isarchive)
    signals.article_writer_finalized.connect(archivemaker)
    signals.article_writer_finalized.connect(photoarchivelist)
