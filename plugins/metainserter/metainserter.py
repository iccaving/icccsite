from pelican import signals
from pelican.contents import Article
import logging
import re
import os

from pelican.writers import Writer, is_selected_for_writing


def MetaInserter(pelican):
    return MetaWriter


class MetaWriter(Writer):

    def write_file(self, name, template, context, relative_urls=False,
                   paginated=None, override_output=False, **kwargs):
        
        # Make sure index page doesn't show articles from subsites
        if name == "index.html":
            paginated['articles'] = [article for article in paginated['articles'] if 'subsite' not in article.metadata.keys()]
            context['articles'] = [article for article in context['articles'] if 'subsite' not in article.metadata.keys()]

        if "article" in kwargs:
            article = kwargs["article"]
            content = article.content
            metadata = article.metadata
            
            # Replace {{ tags }} with the data they should have
            if "data" in dir(article):
                for key in article.data:
                    htmlkey = key.replace(">", "&gt;")
                    content = re.sub(r'({{\s*?)(' + htmlkey + r')(\s*?}})', article.data[key], content)
            modified_article = Article(content, article.metadata, settings=article.settings, source_path=article.source_path, context=context)
            kwargs["article"] = modified_article

            if "subsite" in metadata.keys():
                # Subsite pages are really articles because they can't access the full article list if they're pages for some reason
                # so make page = article so the page template can still work
                kwargs["page"] = kwargs["article"]
                print(article.url)

                
                # Make sure subsite pages only display subsite articles
                rel_path = article.source_path.replace(os.path.join(context['PATH'], "_" + metadata['subsite'], ''), '')
                kwargs["articles"] = [article for article in context["articles"] if 'subsite' in article.metadata.keys() and article.metadata['subsite'] == metadata['subsite'] and article.save_as != os.path.join(metadata['subsite'], "index.html") and not article.metadata['ispage']]
            else:
                # Make sure non-subsite pages only display non-subsite articles
                kwargs["articles"] = [article for article in context["articles"] if 'subsite' not in article.metadata.keys()]

        
        super(MetaWriter, self).write_file(name, template, context, relative_urls=relative_urls, paginated=paginated, override_output=False, **kwargs)


def register():
    signals.get_writer.connect(MetaInserter)
