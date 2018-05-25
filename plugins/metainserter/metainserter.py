import logging
import re
import os
from olm.logger import get_logger
from olm.writer import Writer

logger = get_logger('olm.plugins.metainserter')

def meta_inserter_lots(sender, context):
    for source in context['all_files']:
        meta_inserter(context, source)

def meta_inserter_one(sender, context, source):
    meta_inserter(context, source)

def meta_inserter(context, source):
    if hasattr(source, 'same_as_cache'):
        if source.same_as_cache and context.caching_enabled:
            return
    metadata = source.metadata

    # Useful bit of metadata to have access to
    if source.source_filepath is not None:
        metadata['source_path'] = source.source_filepath.replace(os.path.join(os.getcwd(), ""), "")

    # Replace {{ tags }} with the data they should have
    def replacer(match):
        key = match.group(1).strip().replace("&gt;", ">")

        if 'data' in dir(source) and key in source.data:
            return source.data[key] + "\n"
        elif key in context:
            return context[key] + "\n"
        else:
            logger.warn("Failed to replace %s in file '%s %s'", match.group(0), source.date.strftime('%Y-%m-%d'), source.title)
            return match.group(0)

    pattern = re.compile(r'{{(.*?)}}')
    
    source.content = pattern.sub(replacer, source.content)

    #if source.content is not '' and source.source_filepath is not None and 'caves' in source.source_filepath:
    #    print(source.source_filepath)
    #    print(source.content)

def register():
    return [("BEFORE_MD_CONVERT", meta_inserter_one)]
