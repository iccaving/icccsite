from pelican import signals
import logging
import re
from functools import partial
from bs4 import BeautifulSoup
import ast
import json
import codecs
import os

def MetaInserter(path, context):
    # The obvious place mentioned in the readme.
    if "article" in path or "caves" in path:
        # Open html file. Check for metadata
        # logging.critical(str(path))
        soup = BeautifulSoup(open(path), "html.parser")
        if soup.find("script", {"id": "metadata"}) is not None:
            # Extract the metadata and interpret it as a dictionary
            temp = ''
            for item in soup.find("script", {"id": "metadata"}).contents:
                temp += item
            metadata = ast.literal_eval(temp.strip())

            # Remove the metadata so it doesn't appear on the live site
            [x.extract() for x in soup.findAll("script", {"id": "metadata"})]

            # Clean up empty tags often left by markdown
            empty_tags = soup.findAll(lambda tag: tag.name == 'p' and not tag.contents and (
                tag.string is None or not tag.string.strip()))
            [empty_tag.extract() for empty_tag in empty_tags]

            html = soup.prettify()

            # This gets rid of the paragraph tags that markdown places round our
            # tags
            html = re.sub(r'<p>\s*?(({{\s*?\w*\s*?}}\s*)*)\s*?</p>', '\g<1>', html)

            for key in metadata:
                # For each key in the metadata check if there is an appropriate tag in
                # in the rest of the file and if there is replace the tag with
                # the data

                htmlkey = key.replace(">", "&gt;")
                html = re.sub(
                    r'({{\s*?)(' + htmlkey + r')(\s*?}})', metadata[key], html)

            with codecs.open(path, 'w', 'utf-8') as f:
                f.write(html)

def register():
    signals.content_written.connect(MetaInserter)
