#Markdown Extension
import markdown
from markdown.inlinepatterns import Pattern

image = r'.*?(\[\!|\[).*?(image).*?(".*?").*?((?:[a-z][a-z]+)).*?(\])'

class AttrTagPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern and with the html attributes defined with the constructor.

    """
    def __init__ (self, pattern, md):
        Pattern.__init__(self, pattern)
        self.md = md

    def handleMatch(self, m):
        outer = markdown.util.etree.Element('a')
        el = markdown.util.etree.SubElement(outer, 'img')
        if m.group(2) == '[!':
            el.set('src', m.group(4).replace('"','').replace('\'',''))
            outer.set('href', m.group(4).replace('"','').replace('\'',''))
        elif m.group(2) == '[':
            el.set('src', self.md.Meta['photoarchive'][0].encode("utf-8") + '/' + m.group(4).replace('"','').replace('\'',''))
            outer.set('href', self.md.Meta['photoarchive'][0].encode("utf-8") + '/?image=' + m.group(4).replace('"','').replace('\'','').replace('--thumb',''))
        if m.group(5) == 'center':
            el.set('class', 'article-img-center')
        elif  m.group(5) == 'left':
            el.set('class', 'article-img-left')
        elif  m.group(5) == 'right':
            el.set('class', 'article-img-right')
        elif  m.group(5) == 'big':
            el.set('class', 'article-img-big')
        return outer

class InlinePhotos(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        tag = AttrTagPattern(image, md)
        md.inlinePatterns.add('inlineimg', tag, '_begin')

def makeExtension(configs=None):
    return InlinePhotos(configs=configs)
