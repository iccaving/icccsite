from collections import namedtuple
import os
import re
import time
from datetime import datetime
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

from olm.source import Source
from olm.writer import Writer
from olm.logger import get_logger
from olm.helper import merge_dictionaries
from olm.signals import Signal, signals
from olm.constants import ArticleStatus

from util import parse_metadata

logger = get_logger('olm.plugins.cavepeep')

class Cave(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cave_articles = []

    def write_file(self, context=None):
        if self.context.caching_enabled and self.same_as_cache:
            return
        try:
            super().write_file(
                context,
                content=context.MD(self.content),
                metadata=self.metadata,
                cave_articles=sorted(self.cave_articles, key=lambda x: x[0].date, reverse=True),
                pagename=self.basename)
        except Exception as e:
            logger.warn("Failed to write {}".format(self.output_filepath))
            logger.warn(e)
        return not self.same_as_cache

class Caver(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caver_articles = []
        self.cocavers = []
        self.caves = []
        self.authored = None
        self.number = 0

    def write_file(self, context=None):
        if self.context.caching_enabled and self.same_as_cache:
            return
        try:
            super().write_file(
                context,
                content=context.MD(self.content),
                metadata=self.metadata,
                caver_articles=sorted(self.caver_articles, key=lambda x: x.date, reverse=True),
                personname=self.basename,
                authored=self.authored,
                cocavers=self.cocavers,
                caves=self.caves,
                number=self.number)
        except Exception as e:
            logger.warn("Failed to write {}".format(self.output_filepath))
            logger.warn(e)
        return not self.same_as_cache

def parse_changes(metadata):
    trips = parse_metadata(metadata)
    people = set([ person for trip in trips for person in trip['people'] ])
    caves = set([ cave for trip in trips for cave in trip['caves'] ])
    return (people, caves)

def construct_bios(sender, context, **kwargs):
    time_start = time.time()
    contentpath=context.SOURCE_FOLDER
    logger.debug("Cavebios starting")

    def get_bios(btype):
        path = os.path.join(contentpath, btype)
        dictionary = {}
        for dirpath, dirnames, filenames in os.walk(path):
            for afile in filenames:
                logger.debug("Cavebios: Reading {}/{}".format(dirpath, afile))
                if btype == "caves":
                    article = Cave(context, os.path.join(dirpath, afile))
                    article.type = "cave"
                else:
                    article = Caver(context, os.path.join(dirpath, afile))
                    article.type = "caver"
                article.data = get_data_from_metadata(article.metadata)
                article.cache_id = afile
                article.cache_type = btype.upper()
                context['all_files'].append(article)
                dictionary[os.path.splitext(afile)[0]]=article
                context[btype + '_db'].insert({"name": os.path.splitext(afile)[0],  "article": article})

        return dictionary

    context['caves_db'] = TinyDB(storage=MemoryStorage)
    context['cavers_db'] = TinyDB(storage=MemoryStorage)

    context['caverbios']= get_bios("cavers")
    context['cavebios'] = get_bios("caves")
    logger.info("Processed cave and caver bios in %.3f seconds", (time.time() - time_start))

def get_data_from_metadata(metadata):
    data = {}
    for key in metadata.keys():
        if key == "location":
             data["map"] = """<div class="padmore"><iframe width="100%" height="450" frameborder="0" style="border:0" allowfullscreen src="https://www.google.com/maps/embed/v1/search?q=""" + re.sub(r',\s*', "%2C", metadata["location"].strip()) + """&maptype=satellite&key=AIzaSyB03Nzox4roDjtKoddF9xFcYsvm4vi26ig" allowfullscreen></iframe></div>"""
    return data

def was_author_in_cave(article, cave_name):
    if 'cavepeeps' not in article.metadata.keys():
        return False
    trips = article.metadata['cavepeeps']
    authors = []
    if 'author' in article.metadata.keys():
        authors = article.metadata['author']
    elif 'authors' in article.metadata.keys():
        authors = article.metadata['authors']
    for trip in trips:
        if cave_name in trip:
            for author in authors:
                if str(author) in trip:
                    return True
    return False

def get_changes(context):
    # Work out if we need to update this file
    changes = context['cache_change_types']
    meta_changes = context['cache_changed_meta']
    changed_caves = []
    changed_people = []
    if "ARTICLE.NEW_FILE" in changes or "ARTICLE.META_CHANGE" in changes:
        for meta_change in meta_changes:
            added, removed, modified = meta_change
            if 'cavepeeps' in added:
                people, caves = parse_changes(added['cavepeeps'])
                changed_people.extend(people)
                changed_caves.extend(caves)
            if 'cavepeeps' in removed:
                people, caves = parse_changes(removed['cavepeeps'])
                changed_caves.extend(caves)
                changed_people.extend(people)
            if 'cavepeeps' in modified:
                people, caves = parse_changes(modified['cavepeeps'][0])
                changed_caves.extend(caves)
                changed_people.extend(people)
                people, caves = parse_changes(modified['cavepeeps'][1])
                changed_caves.extend(caves)
                changed_people.extend(people)
            if 'authors' in added:
                people = [ p.strip() for p in added['authors'].split(',') ]
                changed_people.extend(people)
            if 'authors' in removed:
                people = [ p.strip() for p in removed['authors'].split(',') ]
                changed_people.extend(people)
            if 'authors' in modified:
                people = [ p.strip() for p in modified['authors'][0].split(',') ]
                changed_people.extend(people)                
                people = [ p.strip() for p in modified['authors'][1].split(',') ]
                changed_people.extend(people)
    return changed_caves, changed_people
    
def generate_cave_pages(context):
    changes = context['cache_change_types']
    meta_changes = context['cache_changed_meta']
    refresh_triggers       = ["ARTICLE.NEW_FILE", "ARTICLE.REMOVED_FILE"]
    refresh_meta_triggers  = ['title', 'location', 'date', 'status']
    changed_caves, changed_people = get_changes(context)
    # Flatten list of all caves
    caves = sorted(list(set([ cave for trip in context['trip_db'].all() for cave in trip['caves'] if cave is not None ])))
    # Ensure each has an article object in the db
    for cave_name in caves:
        if context['caves_db'].get(Query().name == cave_name) is None:
            article = Cave(context, content='', metadata={},basename=cave_name)
            article.same_as_cache = context.is_cached
            context['caves_db'].insert({"name": cave_name,  "article": article})

    logger.debug("Writing %s caver pages", len(context['caves_db'].all()))
    number_written = 0
    for cave in context['caves_db']:
        cave_name = cave['name']
                
        # Set filepath and jinja template
        cave['article'].output_filepath = os.path.join("caves", str(cave_name) + '.html')
        cave['article'].template = 'cavepages.html'

        # Construct articles list with useful stuff (date, article, author_in_cave) surfaced
        trips = context['trip_db'].search(Query().caves.any([cave_name]))
        cave['article'].cave_articles = [ (t['article'], t['date'], was_author_in_cave(t['article'], cave_name)) for t in trips ]

        # Work out if it needs writing
        if context.caching_enabled:
            if cave_name in changed_caves:
                cave['article'].same_as_cache = False
            if any(i in changes for i in refresh_triggers):
                cave['article'].same_as_cache = False
            if any(any(m in merge_dictionaries(*c) for m in refresh_meta_triggers) for c in meta_changes):
                cave['article'].same_as_cache = False
            if cave['article'].same_as_cache:
                continue

        number_written = number_written + 1
        signal_sender = Signal("BEFORE_ARTICLE_WRITE")
        signal_sender.send(context=context, afile=cave['article'])
        cave['article'].write_file(context=context)
    logger.info("Wrote %s out of %s total cave pages", number_written, len(context['caves_db'].all()))

    # ==========Write the index of caves================
    cached = True
    if context.caching_enabled:
        if len(changed_caves) > 0:
            cached = False
        if any(i in changes for i in refresh_triggers):
            cached = False
        if any(any(m in merge_dictionaries(*c) for m in refresh_meta_triggers) for c in meta_changes):
            cached = False
        if cached:
            return

    row=namedtuple('row', 'name number recentdate meta')
    rows = []
    for cave in context['caves_db']:
        print(cave)
        name = cave['name']
        number = len(cave['article'].cave_articles)
        recentdate = max([trip[1] for trip in cave['article'].cave_articles])
        meta = cave['article'].metadata
        rows.append(row(name, number, recentdate, meta))
    filename=os.path.join('caves', 'index.html')
    
    writer = Writer(
            context, 
            filename, 
            "cavepages_index.html",
            rows=sorted(rows, key=lambda x: x.name))
    writer.write_file()

def generate_person_pages(context):
    changes = context['cache_change_types']
    meta_changes = context['cache_changed_meta']
    refresh_triggers       = ["ARTICLE.NEW_FILE", "ARTICLE.REMOVED_FILE"]
    refresh_meta_triggers  = ['title', 'location', 'date', 'status']
    changed_caves, changed_people = get_changes(context)
    
    # Flatten list of all cavers
    cavers = sorted(list(set([ person for trip in context['trip_db'].all() for person in trip['people']])))
    # Ensure each caver has an article object in the db

    for caver_name in cavers:
        if context['cavers_db'].get(Query().name == caver_name) is None:
            article = Caver(context, content='', metadata={},basename=caver_name)
            article.same_as_cache = context.is_cached
            context['cavers_db'].insert({"name": caver_name,  "article": article})

    logger.debug("Writing %s caver pages", len(context['cavers_db'].all()))
    number_written = 0
    row=namedtuple('row', 'cave article date')
    for caver in context['cavers_db']:
        caver_name = caver['name']

        # Set filepath and jinja template
        caver['article'].output_filepath = os.path.join("cavers", str(caver_name) + '.html')
        caver['article'].template = 'caverpages.html'

        trips = context['trip_db'].search(Query().people.any([caver_name]))
        caver['article'].caver_articles = [row(' > '.join(t['caves']), t['article'], t['date']) for t in trips ]

        # Set number of trips
        caver['article'].number = len([ t for t in trips if len(t['caves']) > 0 ])

        # Work out it needs to be written
        if context.caching_enabled:
            if caver_name in changed_people:
                caver['article'].same_as_cache = False
            if any(i in changes for i in refresh_triggers):
                caver['article'].same_as_cache = False
            if any(any(m in merge_dictionaries(*c) for m in refresh_meta_triggers) for c in meta_changes):
                caver['article'].same_as_cache = False
            if caver['article'].same_as_cache:
                continue

        # Compute authored
        if caver_name in context.authors:
            authored = [ a for a in context.authors[caver_name] if a.status is not ArticleStatus.DRAFT and a.status is not ArticleStatus.UNLISTED ]
            caver['article'].authored = sorted(authored, key=lambda k: (k.date), reverse=True)

        # Compute cocavers
        cocavers = dict.fromkeys(set([ person for trip in trips for person in trip['people']]),0)
        del cocavers[caver_name]
        for key in cocavers:
            for trip in trips:
                if key in trip['people']:
                    cocavers[key] = cocavers[key] + 1
        caver['article'].cocavers = sorted([(person, cocavers[person]) for person in cocavers.keys()], key=lambda tup: tup[1], reverse=True)

        # Compute caves
        caves = dict.fromkeys(set([ cave for trip in trips for cave in trip['caves']]),0)
        for key in caves:
            for trip in trips:
                if key in trip['caves']:
                    caves[key] = caves[key] + 1
        caver['article'].caves = sorted([(cave, caves[cave]) for cave in caves.keys()], key=lambda tup: tup[1], reverse=True)

        number_written = number_written + 1
        signal_sender = Signal("BEFORE_ARTICLE_WRITE")
        signal_sender.send(context=context, afile=caver['article'])
        caver['article'].write_file(context=context)
    logger.info("Wrote %s out of %s total caver pages", number_written, len(context['cavers_db'].all()))

    # ==========Write the index of cavers================
    cached = True
    if context.caching_enabled:
        if len(changed_people) > 0:
            cached = False
        if any(i in changes for i in refresh_triggers):
            cached = False
        if any(any(m in merge_dictionaries(*c) for m in refresh_meta_triggers) for c in meta_changes):
            cached = False
        if cached:
            return
    row=namedtuple('row', 'name number recentdate meta')
    rows = []
    for caver in context['cavers_db']:
        name = caver['name']
        number = caver['article'].number
        recentdate = max([article.date for article in caver['article'].caver_articles])
        meta = caver['article'].metadata
        rows.append(row(name, number, recentdate, meta))
    filename=os.path.join('cavers','index.html')
    writer = Writer(
        context, 
        filename, 
        "caverpages_index.html",
        rows=sorted(sorted(rows, key=lambda x: x.name), key=lambda x: x.recentdate, reverse=True))
    writer.write_file()

