from functools import partial
import re
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

image = re.compile(r'(\{!|\{)(".*?")?.*?((?:[a-z][a-z]+))(\})(\()(.*?)(\))')

def handleMatch(m, metadata):
    figure = etree.Element('figure')
    a = etree.SubElement(figure, 'a')
    img = etree.SubElement(a, 'img')
    if m.group(2) is not None:
        cap = etree.SubElement(figure, 'figcaption')
        capa = etree.SubElement(cap, 'a')
    else:
        cap = etree.Element('figcaption')
        capa = etree.Element('a')
    if m.group(1) == '{!':
        if len(m.group(6).split(",")) > 1:
            img.set('src', m.group(6).split(",")[0].strip())
            a.set('href', m.group(6).split(",")[1].strip())
            capa.set('href', m.group(6).split(",")[1].strip())
        else:
            img.set('src', m.group(6).strip())
            a.set('href', m.group(6).strip())
            capa.set('href', m.group(6).strip())
    elif m.group(1) == '{':
        if 'photoarchive' in metadata.keys():
            if metadata['photoarchive'] == '':
                archive_loc = '/rcc/caving/photo_archive/'
                if 'type' in metadata.keys():
                    archive_loc += str(metadata['type']).strip() + 's/'
                if 'location' in metadata.keys() and 'date' in metadata.keys():
                    archive_loc += str(metadata['date']) + '%20-%20' + str(metadata['location']) + '/'
                archive_loc = archive_loc.lower()
            else:
                archive_loc = metadata['photoarchive']
        if len(m.group(6).split(",")) > 1:
            img.set('src', archive_loc + m.group(6).split(",")[0].strip())
            a.set('href', m.group(6).split(",")[1].strip())
            capa.set('href', m.group(6).split(",")[1].strip())
        else:
            img.set('src', archive_loc + m.group(6).strip())
            a.set('href', archive_loc + m.group(6)[:-3].strip() + "html")
            capa.set('href', archive_loc + m.group(6)[:-3].strip() + "html")
    if m.group(2) is not None:
        capa.text = m.group(2)[1:-1]
    if m.group(3) == 'center':
        figure.set('class', 'article-img-center')
    elif  m.group(3) == 'left':
        figure.set('class', 'article-img-left')
    elif  m.group(3) == 'right':
        figure.set('class', 'article-img-right')
    return etree.tostring(figure, encoding="unicode", method='xml')

def transform(sender, context, Writer):
    for afile in context['all_files']:
        afile.content = image.sub(partial(handleMatch,metadata=afile.metadata), afile.content)

def register():
    return [
        ("BEFORE_WRITING", transform)
        ]
