from pelican import signals

def isarchive(generator):
    archives = []
    for article in generator.articles:
        archive_loc = ''
        print "Photoarchive: checking article " + article.title
        if 'photoarchive' in article.metadata.keys():
            if article.photoarchive == '':
                archive_loc = 'photo_archive/'
                if 'triportour' in article.metadata.keys():
                    archive_loc += article.triportour + '/'
                if 'location' in article.metadata.keys() and 'date' in article.metadata.keys():
                    archive_loc += article.date.strftime('%Y-%m-%d') + ' - ' + article.location + '/'
                article.metadata['archiveloc'] = archive_loc
                article.archiveloc = archive_loc
            else:
                article.metadata['archiveloc'] = article.photoarchive + '/'
                article.archiveloc = article.photoarchive + '/'
            archives.append((article.archiveloc, article.title, article.date.strftime('%d-%m-%Y')))
    generator.context['photoarchives'] = archives

def archivemaker(generator, writer):
    template = generator.get_template('photoindex')
    filename = "photo_archive/index_template.php"
    writer.write_file(filename, template, generator.context)
    print "Photoarchive: Generic photo archive page generated"
    '''
    for article in generator.articles:
        if 'archiveloc' in article.metadata.keys():
            print "Photoarchive: creating photoarchive directory and index file for " + article.title
            filename = article.metadata['archiveloc'] + 'index.php'
            writer.write_file(filename, template, generator.context)
    '''

def photoarchivelist(generator, writer):
    template = generator.get_template('photoarchivelist')
    filename = "photo_archive/index.php"
    writer.write_file(filename, template, generator.context)
    print "Photoarchive: Photo archive list page generated"



def register():
    signals.article_generator_finalized.connect(isarchive)
    signals.article_writer_finalized.connect(archivemaker)
    signals.article_writer_finalized.connect(photoarchivelist)
