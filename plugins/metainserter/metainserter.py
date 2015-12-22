from pelican import signals
import logging
import re
from functools import partial
from bs4 import BeautifulSoup
import ast
import json
import codecs
import os


def replacer(value, matchobj):
    out = ''
    # Format the metadata for output to the file
    if matchobj.group(2) == "allpeople":
        for index, person in enumerate(ast.literal_eval(value)):
            if index > 0:
                out += ', '
            out += """<a href="/cavers/""" + \
                person.replace(" ", "%20") + """.html">""" + \
                person + """</a>"""
    elif matchobj.group(2) == "mainimg":
        out += """<div class='mainimg'><a href='""" + \
            os.path.split(
                value)[0] + """'><img src='""" + value + """'></a></div>"""
    return out


def MetaInserter(path, context):
    if "article" in path:
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
            [x.extract() for x in soup.findAll("span", {"id": "metadata"})]

            # Clean up empty tags often left by markdown
            empty_tags = soup.findAll(lambda tag: tag.name == 'p' and not tag.contents and (
                tag.string is None or not tag.string.strip()))
            [empty_tag.extract() for empty_tag in empty_tags]

            html = soup.prettify()
            for key in metadata:
                # For each key in the metadata check if there is an appropriate tag in
                # in the rest of the file and if there is replace the tag with
                # the data
                # If the tag is on a line on its own then markdown will wrap it
                # with p tags so the first substituion tests for those and
                # removes the p tags
                html = re.sub(
                    '(<p>\s*?{{\s*?)(' + key + ')(\s*?}}\s*?</p>)', metadata[key], html)
                html = re.sub(
                    '({{\s*?)(' + key + ')(\s*?}})', metadata[key], html)
            with codecs.open(path, 'w', 'utf-8') as f:
                f.write(html)

def register():
    signals.content_written.connect(MetaInserter)
