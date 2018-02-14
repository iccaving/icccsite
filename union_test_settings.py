import os

SETTINGS = {
    'SOURCE_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'content'),
    'OUTPUT_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'output'),
    'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'css'),
    'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'js'),
    'ARTICLE_TYPES': ['trip', 'tour'],
    'INDEX_TYPES': ['index', 'stickyindex'],
    'PLUGINS': ['inlinephotos', 'acyear', 'cavepeeps', 'photoarchive', 'metainserter', 'oldurl', 'wiki'],
    'NO_SCAN': ['wiki','caves','cavers'],
    'PHOTO_LOCATION': 'https://union.ic.ac.uk/rcc/caving/photo_archive/',
    'ASSET_LOCATION': 'https://union.ic.ac.uk/rcc/caving/assets/',
    'SITEURL': "/rcc/caving/source/output",
    'PHOTOREEL': True,
    "BADGES": {
        'lightning': {
            'src': 'lightning.png',
            'alt': 'In the bivi'
        }
    },
    "PAGE_REFRESH_META": ['title', 'location', 'date'],
    "ARTICLE_REFRESH_META": ['title', 'location', 'date'],
    "SUBSITES": {
        "newzealand": {
            'PLUGINS': ['inlinephotos', 'photoarchive', 'metainserter'],
            'TEMPLATES_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'templates', 'subsites', 'newzealand'),
            'CSS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'newzealand', 'css'),
            'JS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'newzealand', 'js'),            
            'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'newzealand', 'css'),
            'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'newzealand', 'js'),
            'ARTICLE_TYPES': [None],
            'BASEURL': '/rcc/caving',
            'SITEURL': "/rcc/caving/source/output/newzealand",
            'PHOTOREEL': False,
            'ARTICLE_SLUG': '{basename}.html'
        },
        "slovenia" : {
            'PLUGINS': ['inlinephotos', 'photoarchive', 'metainserter'],
            'TEMPLATES_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'templates', 'subsites', 'slovenia'),
            'CSS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'slovenia', 'css'),
            'JS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'slovenia', 'js'),            
            'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'slovenia', 'css'),
            'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'slovenia', 'js'),
            'ARTICLE_TYPES': ['expedition'],
            'BASEURL': '/rcc/caving',
            'SITEURL': "/rcc/caving/source/output/slovenia",
            'PHOTOREEL': False,
            'ARTICLE_SLUG': '{date}-{location}.html'
        }
    }
}
