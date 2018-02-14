import logging
import re
import os
from olm.logger import get_logger

logger = get_logger('olm.plugins.metainserter')

def meta_inserter(sender, context, Writer):
    for afile in context['all_files']:
        if hasattr(afile, 'same_as_cache'):
            if afile.same_as_cache:
                continue
        content = afile.content
        metadata = afile.metadata

        # Useful bit of metadata to have access to
        if afile.source_filepath is not None:
            metadata['source_path'] = afile.source_filepath.replace(os.path.join(os.getcwd(), ""), "")

        # Replace {{ tags }} with the data they should have
        def replacer(match):
            key = match.group(1).strip().replace("&gt;", ">")
            
            if 'data' in dir(afile) and key in afile.data:
                return afile.data[key]
            elif key in context:
                return context[key]
            else:
                logger.warn("Failed to replace %s in file '%s %s'", match.group(0), afile.date.strftime('%Y-%m-%d'), afile.title)
                return match.group(0)

        pattern = re.compile(r'{{(.*?)}}')
        content = pattern.sub(replacer, content)

        afile.content = content

def register():
    return ("BEFORE_WRITING", meta_inserter)
