#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'ICCC'
SITENAME = u'Imperial College Caving Club'
#SITEURL = 'https://union.ic.ac.uk/rcc/caving/topsecret'
SITEURL = ''

THEME = 'themes/NZTheme'

PATH = 'content'

STATIC_PATHS = ['assets', 'photo_archive']

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

USE_FOLDER_AS_CATEGORY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = False

DEFAULT_DATE_FORMAT = '%d-%m-%Y'

PLUGIN_PATHS = ["plugins"]
PLUGINS = ['photoarchive', 'saveoldnz', 'inlinephotos']

SLUGIFY_SOURCE = 'basename'

ARTICLE_EXCLUDES = ['oldnz']

ARTICLE_URL = 'articles/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{slug}.html'

FAVICON = "assets/iclogo.png"
