from functools import partial
import re
import os

try:
    # Is the C implementation of ElementTree available?
    import xml.etree.cElementTree as etree
    from xml.etree.ElementTree import Comment
    # Serializers (including ours) test with non-c Comment
    etree.test_comment = Comment
    if etree.VERSION < "1.0.5":
        raise RuntimeError("cElementTree version 1.0.5 or higher is required.")
except (ImportError, RuntimeError):  # pragma: no cover
    # Use the Python implementation of ElementTree?
    import xml.etree.ElementTree as etree
    if etree.VERSION < "1.1":
        raise RuntimeError("ElementTree version 1.1 or higher is required")

strike = re.compile(r'~~(.*?)~~')

def handleMatch(m, metadata):
    delel = etree.Element('del') 
    delel.text = m.group(1)
    return etree.tostring(delel, encoding="unicode", method='xml')

def transform(sender, context):
    for afile in context['all_files']:
        afile.content = strike.sub(partial(handleMatch,metadata=afile.metadata), afile.content)

def register():
    return [
        ("BEFORE_WRITING", transform)
        ]
