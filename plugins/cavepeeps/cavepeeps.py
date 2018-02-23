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

logger = get_logger('olm.plugins.cavepeep')

# =====================Functions============================

def parse_metadata(metadata, article):
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
    for entry in article_metadata:
            # Create key/value relationship between trip identifier (Date + Cave) and list of cavers
            item_date = None
            item_caves = None
            item_people = None
            m = c.match(entry)
            try:
                item_date=datetime.strptime(m.group(1), '%Y-%m-%d')
                item_caves=m.group(2)
                item_people=m.group(3).split(',')
            except AttributeError:
                logger.error(
                            "\nCavepeep metdata error in article: " + article.title + " " + str(article.date.strftime('%Y-%m-%d')) +
                    "\nLine: " + entry +
                    "\nAre DATE, PEOPLE, CAVE present and spelt correctly? Are there semicolons (not colons) seperating each section?" +
                    "\nIf there's no cavepeep data please delete the row from the metadata.")
                continue

            item_people=item_people if type(item_people) is list else [item_people]
            item_people=[x.strip() for x in item_people]

            n = 1
            insert_key = "DATE=" + item_date.strftime('%Y-%m-%d') +"; CAVE=" + item_caves + ";"
            while (insert_key + str(n)) in trips_for_insert:
                n = n + 1
            trips_for_insert[insert_key + str(n)] = item_people

            for person in item_people:
                cavepeep.append(row(item_date, item_caves, person, article))
    return (cavepeep, trips_for_insert)


def article_link(cavepeep_partial, trips_for_insert, article, context):
    # Function to create lists of people on individual trips
    # and making those lists available to the article as a nice html string

    trips = {}
    all_people = set()
    for index, item in enumerate(cavepeep_partial):
        name = item.person
        # Create unique id for trip (essentially a copy/paste of the metadata)
        # An use this to identify a list of people on that trip
        tripid='DATE={0}; CAVE={1};'.format(item.date.strftime('%Y-%m-%d'), item.cave)
        html = """<a href='{0}/cavers/{1}.html'>{2}</a>""".format(context.SITEURL, quote(name), name)
        if tripid in trips.keys():
            trips[tripid] += ", {}".format(html)
        else:
            trips[tripid] = html
        # Also create a list of everyone on any trip
        all_people.add(html)

    # The metadata might need to be used to replace a tag in the article
    # so add it to the metadata item that will be available to metainserter
    if "data" not in dir(article):
        article.data = {}

    article.data["allpeople"] = ', '.join(sorted(list(all_people)))
    for key in trips:
        article.data[key] = trips[key]

    for key in trips_for_insert:
        html = ""
        for index, name in enumerate(trips_for_insert[key]):
            if index == 0:
                html = "<a href='{0}/cavers/{1}.html'>{2}</a>""".format(context.SITEURL, quote(name), name)
            else:
                html += ", {}".format("""<a href='{0}/cavers/{1}.html'>{2}</a>""".format(context.SITEURL, quote(name), name))
        article.data[key] = html

#======================MAIN==========================


def cavepeep_linker_initialise(sender, context):
    context['cavepeep'] = []


def cavepeep_linker_for_each_article(sender, context, article):
    cavepeep_partial = None
    if 'status' in article.metadata.keys() and article.metadata['status'] == ArticleStatus.DRAFT:
        return
    # If the article has the cavepeeps metadata
    if 'cavepeeps' in article.metadata.keys():
        # Parse metadata and return a list where each item contains a date,
        # cave, caver, and article reference
        cavepeep_partial, trips_for_insert =parse_metadata(article.metadata['cavepeeps'], article)
        article_link(cavepeep_partial, trips_for_insert, article, context)

    # If unlisted DO NOT ADD TO MAIN CAVEPEEPS dictionary.
    if 'cavepeeps' in article.metadata.keys() and article.status != ArticleStatus.UNLISTED:
        context['cavepeep'] += cavepeep_partial




def cavepeep_linker_final(sender, context, Writer):
    time_start = time.time()
    cavepeep=context['cavepeep']
    cavepeep.sort(key=lambda tup: tup.date, reverse=True)
    cavepeep.sort(key=lambda tup: tup.person)  # Sort the list by person name
    cavepeep_person=OrderedDict()
    # Add the entries to an ordered dictionary so that for each person
    # (the key) there is a list of tuples containing the cavename, the article
    # its mentioned in, and the specific date of the cave visit
    row=namedtuple('row', 'cave article date')
    for item in cavepeep:
        cavepeep_person.setdefault(item.person, []).append(
            row(item.cave, item.article, item.date))

    cavepeep.sort(key=lambda tup: tup.cave)  # Sort the list by cave name
    flag=False
    cavepeep_cave=OrderedDict()
    # Add the entries to an ordered dictionary so that for each cave (the key) there is a list
    # containing articles its mentioned in. As two people can mention the same cave in the same
    # article there is also duplicate checking so that the same article is not linked twice for
    # cave
    row=namedtuple('row', 'article date')
    for item in cavepeep:
        if item.cave in cavepeep_cave:
            for art, date in cavepeep_cave[item.cave]:
                if item.article == art and item.date == date:
                    flag=True
        if flag is False:
            #logging.debug("Cavepeeps: Adding {} to cavepeep_cave dictionary".format(item.cave))
            cavepeep_cave.setdefault(item.cave, []).append(
                row(item.article, item.date))
        else:
            flag=False

    # Add the dictionaries to the global context (makes them accessible to
    # other plugins and the templates)
    context['cavepeep_cave']=cavepeep_cave
    context['cavepeep_person']=cavepeep_person

    logger.info("Processed cavepeeps in %.3f seconds", (time.time() - time_start))

    time_start = time.time()
    generate_cave_pages(context, Writer)
    logger.info("Cave pages written in %.3f seconds", (time.time() - time_start))

    time_start = time.time()
    generate_person_pages(context, Writer)
    logger.info("Caver pages written in %.3f seconds", (time.time() - time_start))

def register():
    return [
        ("INITIALISED", cavepeep_linker_initialise),
        ("BEFORE_CACHING", construct_bios),
        ("AFTER_ARTICLE_READ", cavepeep_linker_for_each_article),
        ("BEFORE_WRITING", cavepeep_linker_final)
    ]