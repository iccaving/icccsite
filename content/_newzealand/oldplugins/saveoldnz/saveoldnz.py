from pelican import signals
import shutil

def copier(generator, writer):
    content = generator.settings['PATH'] + '/'
    output = generator.settings['OUTPUT_PATH'] + '/'
    shutil.copy2(content + 'oldnz/newzealand-2010-10-15.php', output + 'newzealand-2010-10-15.php')
    shutil.copy2(content + 'oldnz/newzealand-2010-10-15.jpg', output + 'newzealand-2010-10-15.jpg')

def register():
    signals.article_writer_finalized.connect(copier)