from pelican import signals
from pelican.contents import Article
import logging
import re
#from functools import partial
#from bs4 import BeautifulSoup
#import ast
#import json
#import codecs
import os

from pelican.writers import Writer, is_selected_for_writing

def MetaInserter(pelican):
    return MetaWriter

class MetaWriter(Writer):
    def write_file(self, name, template, context, relative_urls=False,
                   paginated=None, override_output=False, **kwargs):
        #for thing in context:
        #    print(context)
        if "article" in kwargs:
            article = kwargs["article"]
            content = article.content
            if "data" in dir(article):
                for key in article.data:
                    htmlkey = key.replace(">", "&gt;")
                    content=re.sub(r'({{\s*?)(' + htmlkey + r')(\s*?}})', article.data[key], content)
            modified_article = Article(content, article.metadata, settings=article.settings, source_path=article.source_path, context=context)
            kwargs["article"] = modified_article
        super(MetaWriter, self).write_file(name, template, context, relative_urls=relative_urls, paginated=paginated, override_output=False, **kwargs)

def register():
    signals.get_writer.connect(MetaInserter)
