import os

SETTINGS = {
    'SITENAME': 'Imperial College Caving Club',
    'SOURCE_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'content'),
    'OUTPUT_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'output'),
    'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'css'),
    'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'js'),
    'ARTICLE_TYPES': ['trip', 'tour'],
    'INDEX_TYPES': ['index', 'stickyindex'],
    'PLUGINS': ['inlinephotos', 'acyear', 'cavepeeps', 'photoarchive', 'metainserter', 'oldurl', 'wiki', 'strikethrough'],
    'NO_SCAN': ['wiki','caves','cavers'],
    'PHOTO_LOCATION': 'https://union.ic.ac.uk/rcc/caving/photo_archive/',
    'ASSET_LOCATION': 'https://union.ic.ac.uk/rcc/caving/assets/',
    'FAVICON': 'assets/iclogo.png',
    'SITEURL': "",
    'PHOTOREEL': True,
    'PHOTOREEL_NUM_ARTICLES': 6,
    "BADGES": {
        'lightning': {
            'src': 'lightning.png',
            'alt': 'In the bivi'
        }
    },
    "ARTICLE_WRITE_TRIGGERS": ["ARTICLE.NEW_FILE", "ARTICLE.REMOVED_FILE"],
    "ARTICLE_META_WRITE_TRIGGERS": ['title', 'location', 'date', 'status', 'summary'],
    "PAGE_WRITE_TRIGGERS": ["ARTICLE.NEW_FILE", "ARTICLE.REMOVED_FILE"],
    "PAGE_META_WRITE_TRIGGERS": ['title', 'location', 'date', 'status'],
    "INDEX_WRITE_TRIGGERS": ["ARTICLE.NEW_FILE", "ARTICLE.REMOVED_FILE"],
    "INDEX_META_WRITE_TRIGGERS": ["title", "date", "location", "thumbr", "thumbl", "summary", "status"],
    "SUBSITES": {
        "newzealand": {
            'PLUGINS': ['inlinephotos', 'photoarchive', 'metainserter'],
            'TEMPLATES_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'templates', 'subsites', 'newzealand'),
            'CSS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'newzealand', 'css'),
            'JS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'newzealand', 'js'),            
            'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'newzealand', 'css'),
            'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'newzealand', 'js'),
            'ARTICLE_TYPES': [None],
            'BASEURL': '',
            'SITEURL': "/newzealand",
            'PHOTOREEL': False,
            'ARTICLE_SLUG': '{basename}.html',
            'PAGE_SLUG': '{basename}.html'
        },
        "slovenia" : {
            'PLUGINS': ['inlinephotos', 'photoarchive', 'metainserter'],
            'TEMPLATES_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'templates', 'subsites', 'slovenia'),
            'CSS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'slovenia', 'css'),
            'JS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'slovenia', 'js'),            
            'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'slovenia', 'css'),
            'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'slovenia', 'js'),
            'ARTICLE_TYPES': ['expedition'],
            'BASEURL': '',
            'SITEURL': "/slovenia",
            'PHOTOREEL': False,
            'ARTICLE_SLUG': '{date}-{location}.html'
        }
    }
}
