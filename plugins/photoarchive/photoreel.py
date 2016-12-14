from pelican.contents import Article
from pelican.urlwrappers import Category
from datetime import datetime
import os

def photoreel(generator):
    if 'PHOTOREEL' in generator.settings.keys():
        if generator.settings['PHOTOREEL'] == False:
            return 0
    else:
        return 0
    if 'SITEURL' in generator.settings.keys():
        siteurl = generator.settings['SITEURL']
    else:
        siteurl = ""
    if 'PHOTOREEL_NUM_ARTICLES' in generator.settings.keys():
        maxcount = generator.settings['PHOTOREEL_NUM_ARTICLES']
    else:
        maxcount = 5
    if 'PHOTOREEL_TRANSITION_TIME' in generator.settings.keys():
        transtime = generator.settings['PHOTOREEL_TRANSITION_TIME']
    else:
        transtime = 1
    if 'PHOTOREEL_NEXT_SLIDE_TIME' in generator.settings.keys():
        nextslidetime = generator.settings['PHOTOREEL_NEXT_SLIDE_TIME']
    else:
        nextslidetime = 3
    count = 0
    content = "<div class='photoreel-container'><div class='photoreel-left'><a><img src='/rcc/caving/assets/arrows-left.svg' style='height: 30px;'></a></div>"
    dots = "<div class='photoreel-dots'>"
    for article in generator.articles:
        if 'archiveloc' in article.metadata.keys() and 'mainimg' in article.metadata.keys():
            content += "<div class='photoreel-photo photoreel-photo-" + str(count) + "'><a href='" + siteurl + "/" + article.url + "'><img src='" + os.path.join(article.metadata['archiveloc'], article.metadata['mainimg']) + "'><span class='photoreel-title'>" + article.metadata['title'] + "</span></a></div>"
            dots += "<a class='photoreel-dot photoreel-dot-" + str(count) + "' data-count='" + str(count) + "'></a>"
            count += 1
        if count == maxcount:
            break
    content += "<div class='photoreel-right'><a><img src='/rcc/caving/assets/arrows-right.svg' style='height: 30px;'></a></div>" + dots + "</div></div>"
    content += """
    <link rel="stylesheet" href='""" + siteurl + """/theme/css/photoreel.css' type="text/css" />
    <script>var maxcount = """ + str(maxcount) + """;var transtime = """ + str(transtime) + """;var nextslidetime = """ + str(nextslidetime) + """;</script>
    <script src='""" + siteurl + """/theme/js/photoreel.js'></script>
    """

    metadata = { 'title':'Imperial College Caving Club',
                 'date': datetime.strptime('9999-12-31', '%Y-%m-%d'),
                 'category': Category('Photo Reel', generator.settings),
                 'type': 'stickyindex',
                 'save_as': 'articles/photo-reel.html'
                }
    generator.articles.insert(0,  Article(content, metadata))
