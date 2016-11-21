# Markdown Extension
import markdown
from markdown.inlinepatterns import Pattern

image = r'(\{!|\{)(".*?")?.*?((?:[a-z][a-z]+))(\})(\()(.*?)(\))'

class AttrTagPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern and with the html attributes defined with the constructor.
    """
    def __init__ (self, pattern, md):
        Pattern.__init__(self, pattern)
        self.md = md

    def handleMatch(self, m):
        figure = markdown.util.etree.Element('figure')
        a = markdown.util.etree.SubElement(figure, 'a')
        img = markdown.util.etree.SubElement(a, 'img')
        cap = markdown.util.etree.SubElement(figure, 'figcaption')
        capa = markdown.util.etree.SubElement(cap, 'a')
        if m.group(2) == '{!':
            if len(m.group(7).split(",")) > 1:
                img.set('src', m.group(7).split(",")[0].strip())
                a.set('href', m.group(7).split(",")[1].strip())
                capa.set('href', m.group(7).split(",")[1].strip())
            else:
                img.set('src', m.group(7).strip())
                a.set('href', m.group(7).strip())
                capa.set('href', m.group(7).strip())
        elif m.group(2) == '{':
            archive_loc = '/rcc/caving/photo_archive/'
            if 'type' in self.md.Meta.keys():
                archive_loc += str(self.md.Meta['type'][0]) + 's/'
            if 'location' in self.md.Meta.keys() and 'date' in self.md.Meta.keys():
                archive_loc += str(self.md.Meta['date'][0]) + '%20-%20' + str(self.md.Meta['location'][0]) + '/'
            archive_loc = archive_loc.lower()
            if len(m.group(7).split(",")) > 1:
                img.set('src', archive_loc + m.group(7).split(",")[0].strip())
                a.set('href', m.group(7).split(",")[1].strip())
                capa.set('href', m.group(7).split(",")[1].strip())
            else:
                img.set('src', archive_loc + m.group(7).strip())
                a.set('href', archive_loc + m.group(7)[:-3].strip() + "html")
                capa.set('href', archive_loc + m.group(7)[:-3].strip() + "html")
        if m.group(3) is not None:
            capa.text = m.group(3)[1:-1]
        if m.group(4) == 'center':
            figure.set('class', 'article-img-center')
        elif  m.group(4) == 'left':
            figure.set('class', 'article-img-left')
        elif  m.group(4) == 'right':
            figure.set('class', 'article-img-right')
        return figure

class InlinePhotos(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        tag = AttrTagPattern(image, md)
        md.inlinePatterns.add('inlineimg', tag, '<image_link')

def makeExtension(configs=None):
    return InlinePhotos(configs=configs)
