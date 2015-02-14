#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Stores Gnomes'
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

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

DEFAULT_DATE_FORMAT = '%d-%m-%Y'

PLUGIN_PATHS = ["plugins", "plugins"]
PLUGINS = ['photoarchive']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL = 'articles/{slug}.html'
ARTICLE_SAVE_AS = 'articles/{slug}.html'
