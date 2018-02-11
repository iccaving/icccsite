import os

SETTINGS = {
    'ARTICLE_TYPES': ['trip', 'tour'],
    'INDEX_TYPES': ['index', 'stickyindex'],
    'PLUGINS': ['inlinephotos', 'acyear', 'cavepeeps', 'photoarchive', 'metainserter', 'oldurl', 'wiki'],
    'NO_SCAN': ['wiki','caves','cavers'],
    'PHOTO_LOCATION': 'https://union.ic.ac.uk/rcc/caving/photo_archive/',
    'ASSET_LOCATION': 'https://union.ic.ac.uk/rcc/caving/assets/',
    'SITEURL': "",
    'PHOTOREEL': True,
    "BADGES": {
        'lightning': {
            'src': 'lightning.png',
            'alt': 'In the bivi'
        }
    },
    "SUBSITES": {
        "newzealand": {
            'PLUGINS': ['inlinephotos', 'photoarchive', 'metainserter'],
            'TEMPLATES_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'templates', 'subsites', 'newzealand'),
            'CSS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'newzealand', 'css'),
            'JS_FOLDER': os.path.join('{{ BASE_FOLDER }}', 'theme', 'static', 'subsites', 'newzealand', 'js'),            
            'OUTPUT_CSS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'newzealand', 'css'),
            'OUTPUT_JS_FOLDER': os.path.join('{{ OUTPUT_FOLDER }}', 'theme', 'subsites', 'newzealand', 'js'),
            'ARTICLE_TYPES': [''],
            'BASEURL': '',
            'SITEURL': "/newzealand",
            'PHOTOREEL': False,
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
        }
    }
}