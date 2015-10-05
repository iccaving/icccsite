#Markdown Extension
import markdown
from markdown.inlinepatterns import Pattern

image = r'(\{!|\{)(".*?")?.*?((?:[a-z][a-z]+))(\})(\()(".*?")(\))'

class AttrTagPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern and with the html attributes defined with the constructor.

    """
    def __init__ (self, pattern, md):
        Pattern.__init__(self, pattern)
        self.md = md

    def handleMatch(self, m):
        a = markdown.util.etree.Element('a')
        figure = markdown.util.etree.SubElement(a, 'figure')
        el = markdown.util.etree.SubElement(figure, 'img')
        if m.group(2) == '{!':
            el.set('src', m.group(7)[1:-1])
            a.set('href', m.group(7)[1:-1])
        elif m.group(2) == '{':
            el.set('src', self.md.Meta['photoarchive'][0] + '/' + m.group(7)[1:-1])
            a.set('href', self.md.Meta['photoarchive'][0] + '/' + m.group(7)[1:-1])
        if m.group(4) == 'center':
            figure.set('class', 'article-img-center')
        elif  m.group(4) == 'left':
            figure.set('class', 'article-img-left')
        elif  m.group(4) == 'right':
            figure.set('class', 'article-img-right')
        if m.group(3) is not None:
            cap = markdown.util.etree.SubElement(figure, 'figcaption')
            cap.text = m.group(3)[1:-1]
        return a

class InlinePhotos(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        tag = AttrTagPattern(image, md)
        md.inlinePatterns.add('inlineimg', tag, '<image_link')

def makeExtension(configs=None):
    return InlinePhotos(configs=configs)
