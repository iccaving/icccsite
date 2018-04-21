import os

def add_cache_type(sender, context, articles):
    for afile in context['all_files']:
        path = afile.relpath.split(os.sep)
        if len(path) > 0 and 'index' == path[0]:
            afile.cache_type = "INDEX_ARTICLE"


def register():
    return [
        ("BEFORE_CACHING", add_cache_type)
        ]
