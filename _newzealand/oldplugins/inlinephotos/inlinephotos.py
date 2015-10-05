from pelican import signals
from .mdx_inlinephotos import InlinePhotos
import logging


def addInlinePhotos(gen):
    if not gen.settings.get('MD_EXTENSIONS'):
        from pelican.settings import DEFAULT_CONFIG
        gen.settings['MD_EXTENSIONS'] = DEFAULT_CONFIG['MD_EXTENSIONS']

    if InlinePhotos not in gen.settings['MD_EXTENSIONS']:
        gen.settings['MD_EXTENSIONS'].append(InlinePhotos())

    logging.debug("InlinePhotos: Success")

def register():
    signals.initialized.connect(addInlinePhotos)
