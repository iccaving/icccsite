from pelican import signals
import logging

def isarchive(generator):
    archives = []
    for article in generator.articles:
        if 'ROOTLOC' in generator.settings.keys():
            archive_loc = generator.settings['ROOTLOC']
        else:
            archive_loc = ''
        logging.debug("Photoarchive: checking article " + article.title)
        if 'photoarchive' in article.metadata.keys():
            if article.photoarchive == '':
                archive_loc += 'photo_archive/'
                if 'type' in article.metadata.keys():
                    archive_loc += article.type + 's/'
                if 'location' in article.metadata.keys() and 'date' in article.metadata.keys():
                    archive_loc += article.date.strftime('%Y-%m-%d') + '%20-%20' + article.location + '/'
                article.metadata['archiveloc'] = archive_loc.lower()
                article.archiveloc = archive_loc.lower()
                logging.critical(archive_loc)
            else:
                if article.photoarchive[:1] == '/':
                    article.metadata['archiveloc'] = archive_loc + article.photoarchive + '/'
                    article.archiveloc = archive_loc + article.photoarchive + '/'
                else:
                    article.metadata['archiveloc'] = article.photoarchive + '/'
                    article.archiveloc = article.photoarchive + '/'
            archives.append((article.archiveloc, article.title, article.date.strftime('%d-%m-%Y')))
    generator.context['photoarchives'] = archives

def archivemaker(generator, writer):
    template = generator.get_template('photoindex')
    filename = "photo_archive/index_template.php"
    writer.write_file(filename, template, generator.context)
    logging.debug("Photoarchive: Generic photo archive page generated")
    '''
    for article in generator.articles:
        if 'archiveloc' in article.metadata.keys():
            print "Photoarchive: creating photoarchive directory and index file for " + article.title
            filename = article.metadata['archiveloc'] + 'index.php'
            writer.write_file(filename, template, generator.context)
    '''

def photoarchivelist(generator, writer):
    template = generator.get_template('photoarchivelist')
    filename = "photo_archive/index.html"
    writer.write_file(filename, template, generator.context)
    logging.debug("Photoarchive: Photo archive list page generated")



def register():
    signals.article_generator_finalized.connect(isarchive)
    signals.article_writer_finalized.connect(archivemaker)
    signals.article_writer_finalized.connect(photoarchivelist)
