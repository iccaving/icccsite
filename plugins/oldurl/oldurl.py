import os

def getoldurl(sender, context, articles):
    oldurls = []
    for article in articles:  
        # Loop through articles
        # If the article has the oldurl metadata
        if 'oldurl' in article.metadata.keys():
            if article.metadata['oldurl'] is not '':
                oldurls.append(
                    (article.metadata['oldurl'], context["SITEURL"] + "/" + article.url))
    context['oldurls'] = oldurls


def generatehtaccess(sender, context, Writer):
    filename=os.path.join(context.OUTPUT_FOLDER, '.htaccess')
    writer = Writer(
        context, 
        filename, 
        'htaccess.html',
       )
    writer.write_file()

def register():
    return [
        ("AFTER_ALL_ARTICLES_READ", getoldurl),
        ("BEFORE_WRITING", generatehtaccess)
    ]