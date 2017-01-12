from pelican import signals
from .mdx_inlinephotos import InlinePhotos
import logging


def addInlinePhotos(gen):
    if not gen.settings.get('MARKDOWN'):
        from pelican.settings import DEFAULT_CONFIG
        gen.settings['MARKDOWN'] = DEFAULT_CONFIG['MARKDOWN']

    if InlinePhotos not in gen.settings['MARKDOWN']['extension_configs']:
        gen.settings['MARKDOWN']['extension_configs'][InlinePhotos()] = ''

    logging.debug("InlinePhotos: Success")


def register():
    signals.initialized.connect(addInlinePhotos)
