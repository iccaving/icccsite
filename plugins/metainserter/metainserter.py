import logging
import re
import os
from olm.logger import get_logger

logger = get_logger('olm.plugins.metainserter')

def meta_inserter(sender, context, article):
    content = article.content
    metadata = article.metadata

    # Useful bit of metadata to have access to
    if article.source_filepath is not None:
        metadata['source_path'] = article.source_filepath.replace(os.path.join(os.getcwd(), ""), "")

    # Replace {{ tags }} with the data they should have
    def replacer(match):
        key = match.group(1).strip().replace("&gt;", ">")
        if key in article.data:
            return article.data[key]
        else:
            logger.warn("Failed to replace %s in file '%s %s'", match.group(0), article.date.strftime('%Y-%m-%d'), article.title)
            return match.group(0)

    if "data" in dir(article):
        pattern = re.compile(r'{{(.*)}}')
        content = pattern.sub(replacer, content)

    article.content = content

def register():
    return ("BEFORE_ARTICLE_WRITE", meta_inserter)
