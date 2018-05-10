from collections import namedtuple, defaultdict, OrderedDict
import os
from datetime import date, datetime
import time
import string
import sys
import re
import copy
from urllib.parse import quote 

from olm.logger import get_logger
from olm.constants import ArticleStatus
from bios import generate_cave_pages, generate_person_pages, construct_bios

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


logger = get_logger('olm.plugins.cavepeep')
 

# =====================Functions============================

def parse_metadata(context, metadata, article):
    # Create list of people, caves they have been to and the articles that the
    # trip is recorded in. Also create array of caves and the articles that
    # refer to the cave (could have a 'people who have been in this cave' thing
    # as well but I didn't think it was useful
    trips_for_insert = {}
    cavepeep = []  # Set up list to hold named tuples
    row = namedtuple('row', 'date cave person article')
    # Ensure the metadata is a list. It will be a string if there is
    # just one entry
    article_metadata = [metadata] if not isinstance(metadata, list) else metadata
    # Look at all the entries. Each will describe a trip that happened
    # on a date.

    c = re.compile(r"""\s*DATE=\s*(\d\d\d\d-\d\d-\d\d)\s*;\s*CAVE=\s*([\s\w\D][^;]*)\s*;\s*PEOPLE=\s*([\s\w\D][^;]*);*[\n\t\r]*""")
    c2 = re.compile(r"""\s*NOCAVE=\s*([\s\w\D][^;]*);*[\n\t\r]*""")
    for entry in article_metadata:
            # Create key/value relationship between trip identifier (Date + Cave) and list of cavers
            item_date = None
            item_caves = None
            item_people = None
            m = c.match(entry)
            m2 = c2.match(entry)
            if m:
                item_date=datetime.strptime(m.group(1), '%Y-%m-%d')
                item_caves=m.group(2)
                item_people=m.group(3).split(',')
            elif m2:
                item_date=article.date
                item_caves=None
                item_people=m2.group(1).split(',')
            else:
                logger.error(
                            "\nCavepeep metdata error in article: " + article.title + " " + str(article.date.strftime('%Y-%m-%d')) +
                    "\nLine: " + entry +
                    "\nAre DATE, PEOPLE, CAVE present and spelt correctly? Are there semicolons (not colons) seperating each section?" +
                    "\nIf there's no cavepeep data please delete the row from the metadata.")
                continue

            item_caves = [] if item_caves is None else item_caves.split('>')
            item_caves = item_caves if type(item_caves) is list else [item_caves]
            item_caves = [x.strip() for x in item_caves ]

            item_people = item_people if type(item_people) is list else [item_people]
            item_people = [x.strip() for x in item_people]

            context['trip_db'].insert({"article": article, "date": item_date, "caves": item_caves, "people": item_people})


def article_link(context, article):
    # Function to create lists of people on individual trips
    # and making those lists available to the article as a nice html string
    if "data" not in dir(article):
        article.data = {}

    def linkify_name(name):
        return """<a href='{0}/cavers/{1}.html'>{2}</a>""".format(context.SITEURL, quote(name), name)

    trips = context['trip_db'].search(Query().article == article)

    # Flatten the lists of people from this article
    all_people = list(set([ person for trip in trips for person in trip['people']]))
    article.data["allpeople"] = ', '.join(sorted(map(linkify_name, all_people)))

    trip_data = {}
    for trip in trips:
        trip_id='DATE={:%Y-%m-%d}; CAVE={};'.format(trip['date'], ' > '.join(trip['caves']))
        trip_people = ', '.join(sorted(map(linkify_name, trip['people'])))
        if trip_id not in article.data:
            article.data[trip_id] = trip_people
        else:
            article.data[trip_id + '1'] = article.data[trip_id]
            n = 2
            while (trip_id + str(n)) in article.data:
                n = n + 1
            article.data[trip_id + str(n)] = article.data[trip_id]


#======================MAIN==========================


def cavepeep_linker_initialise(sender, context):
    context['cavepeep'] = []
    context['trip_db'] = TinyDB(storage=MemoryStorage)


def cavepeep_linker_for_each_article(sender, context, article):
    cavepeep_partial = None
    if 'status' in article.metadata.keys() and article.metadata['status'] == ArticleStatus.DRAFT:
        return

    # If the article has the cavepeeps metadata
    if 'cavepeeps' in article.metadata.keys():
        # Parse metadata and return a list where each item contains a date,
        # cave, caver, and article reference
        parse_metadata(context, article.metadata['cavepeeps'], article)
        article_link(context, article)

    # If unlisted DO NOT ADD TO MAIN CAVEPEEPS dictionary.
    if 'cavepeeps' in article.metadata.keys() and article.status != ArticleStatus.UNLISTED:
        #context['cavepeep'] += cavepeep_partial
        pass

def cavepeep_linker_final(sender, context, articles):
    time_start = time.time()
    cavepeep=context['cavepeep']
    cavepeep_person=OrderedDict()
    row=namedtuple('row', 'cave article date')

    # Flatten the list of people
    people = sorted(list(set([ person for trip in context['trip_db'].all() for person in trip['people']])))
    for person in people:
        for trip in context['trip_db'].search(Query().people.any([person])):
            cave = ' > '.join(trip['caves']) if trip['caves'] != [] else None
            cavepeep_person.setdefault(person, []).append(row(cave, trip['article'], trip['date']))


    cavepeep_cave=OrderedDict()
    # Add the entries to an ordered dictionary so that for each cave (the key) there is a list
    # containing articles its mentioned in. As two people can mention the same cave in the same
    # article there is also duplicate checking so that the same article is not linked twice for
    # cave
    row=namedtuple('row', 'article date')
    caves = sorted(list(set([ cave for trip in context['trip_db'].all() for cave in trip['caves'] if cave is not None ])))
    for cave in caves:
        for trip in context['trip_db'].search(Query().caves.any([cave])):
            cavepeep_cave.setdefault(cave, []).append(row(trip['article'], trip['date']))

    # Add the dictionaries to the global context (makes them accessible to
    # other plugins and the templates)
    context['cavepeep_cave']=cavepeep_cave
    context['cavepeep_person']=cavepeep_person

    logger.info("Processed cavepeeps in %.3f seconds", (time.time() - time_start))

    time_start = time.time()
    generate_cave_pages(context)
    logger.info("Cave pages written in %.3f seconds", (time.time() - time_start))

    time_start = time.time()
    generate_person_pages(context)
    logger.info("Caver pages written in %.3f seconds", (time.time() - time_start))

def register():
    return [
        ("INITIALISED", cavepeep_linker_initialise),
        ("BEFORE_CACHING", construct_bios),
        ("AFTER_ARTICLE_READ", cavepeep_linker_for_each_article),
        ("AFTER_ALL_ARTICLES_READ", cavepeep_linker_final)
    ]