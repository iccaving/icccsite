from datetime import datetime
from olm.article import Article
import os

def photoreel(sender, context, articles):
    if 'PHOTOREEL' in context:
        if context['PHOTOREEL'] == False:
            return 0
    else:
        return 0
    if 'SITEURL' in context:
        siteurl = context['SITEURL']
    else:
        siteurl = ""
    if 'PHOTOREEL_NUM_ARTICLES' in context:
        maxcount = context['PHOTOREEL_NUM_ARTICLES']
    else:
        maxcount = 5
    if 'PHOTOREEL_TRANSITION_TIME' in context:
        transtime = context['PHOTOREEL_TRANSITION_TIME']
    else:
        transtime = 1
    if 'PHOTOREEL_NEXT_SLIDE_TIME' in context:
        nextslidetime = context['PHOTOREEL_NEXT_SLIDE_TIME']
    else:
        nextslidetime = 3
    count = 0
    content = "<div class='photoreel-container'><div class='photoreel-left'><a><img src='" + context['SITEURL'] + "/assets/arrows-left.svg' style='height: 30px;'></a></div>"
    dots = "<div class='photoreel-dots'>"
    for article in articles:
        if 'archiveloc' in article.metadata.keys() and 'mainimg' in article.metadata.keys() and article.type != 'unlisted':
            content += "<div class='photoreel-photo photoreel-photo-" + str(count) + "'><a href='" + siteurl + "/" + article.url + "'><img src='" + os.path.join(article.metadata['archiveloc'], article.metadata['mainimg']) + "'><span class='photoreel-title'>" + article.metadata['title'] + "</span></a></div>"
            dots += "<a class='photoreel-dot photoreel-dot-" + str(count) + "' data-count='" + str(count) + "'></a>"
            count += 1
        if count == maxcount:
            break
    content += "<div class='photoreel-right'><a><img src='" + context['SITEURL'] + "/assets/arrows-right.svg' style='height: 30px;'></a></div>" + dots + "</div>"
    content += """
    <link rel="stylesheet" href='""" + siteurl + """/theme/css/photoreel.css' type="text/css" />
    <script>var maxcount = """ + str(maxcount) + """;var transtime = """ + str(transtime) + """;var nextslidetime = """ + str(nextslidetime) + """;</script>
    <script src='""" + siteurl + """/theme/js/photoreel.js'></script></div>
    """

    metadata = { 'title':'Recent Trips',
                 'date': '9999-12-31',
                 'type': 'stickyindex',
                }
    articles.insert(0,  Article(context, content=content, metadata=metadata, basename='photoreel'))


