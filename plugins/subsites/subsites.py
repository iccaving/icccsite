from pelican import signals
from pelican.readers import MarkdownReader
from pelican.utils import slugify
from pelican import ArticlesGenerator
import os
import datetime

# Create a new reader class, inheriting from the pelican.reader.BaseReader


def add_pages(pel):
    subsites = [name for name in os.listdir(pel.settings['PATH']) if os.path.isdir(os.path.join(pel.settings['PATH'], name)) and name[0] == "_"]
    ##pel.settings['PAGE_PATHS'] = pel.settings['PAGE_PATHS'] + [os.path.join(subsite, 'pages') for subsite in subsites]


class BetterMarkdownReader(MarkdownReader):

    def read(self, filename):
        content, metadata = super(BetterMarkdownReader, self).read(filename)
        rel_path = filename.replace(os.path.join(os.getcwd(), "content", ""), "")
        if rel_path[0] == "_":
            rel_path_split = rel_path.split(os.sep)
            basename = rel_path_split[-1].replace(".md", "")
            subsite = rel_path_split[0][1:]
            page_type = rel_path_split[1]
            template = os.path.join("subsites", subsite, "article")
            save_as = os.path.join(subsite, "articles", slugify(basename) + ".html")
            url = os.path.join(self.settings["SITEURL"], subsite, "articles", slugify(basename) + ".html")
            metadata["ispage"] = False

            if page_type == "pages":
                metadata["date"] = datetime.datetime.strptime("2000-01-01", "%Y-%m-%d")
                template = os.path.join("subsites", subsite, "page")
                save_as = os.path.join(subsite, "pages", slugify(basename) + ".html")
                url = os.path.join(self.settings["SITEURL"], subsite, "pages", slugify(basename) + ".html")
                metadata["ispage"] = True

            if ''.join(rel_path_split[1:]) == "index.md":
                template = os.path.join("subsites", subsite, "index")
                save_as = os.path.join(subsite, "index.html")
                url = os.path.join(self.settings["SITEURL"], subsite, "index.html")
                metadata["slug"] = slugify(subsite + "-" + basename)

            metadata["template"] = template
            metadata["save_as"] = save_as
            metadata["subsite"] = subsite
            metadata["url"] = url

        return content, metadata


def add_reader(readers):
    readers.reader_classes['md'] = BetterMarkdownReader


def register():
    signals.initialized.connect(add_pages)
    signals.readers_init.connect(add_reader)
