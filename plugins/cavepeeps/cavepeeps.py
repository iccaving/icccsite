import os
from datetime import datetime
import time
import re
from urllib.parse import quote 

from olm.logger import get_logger
from olm.constants import ArticleStatus
from bios import generate_cave_pages, generate_person_pages, construct_bios
from util import parse_metadata

logger = get_logger('olm.plugins.cavepeep')
 
# =====================Functions============================
def article_link(context, article, trips):
    # Function to create lists of people on individual trips
    # and making those lists available to the article as a nice html string
    if "data" not in dir(article):
        article.data = {}

    def linkify_name(name):
        return """<a href='{0}/cavers/{1}.html'>{2}</a>""".format(context.SITEURL, quote(name), name)

    # Flatten the lists of people from this article
    all_people = list(set([ person for trip in trips for person in trip['people']]))
    article.data["allpeople"] = ', '.join(sorted(map(linkify_name, all_people)))

    for trip in trips:
        trip_id='DATE={:%Y-%m-%d}; CAVE={};'.format(trip['date'], ' > '.join(trip['caves']))
        trip_people = ', '.join(sorted(map(linkify_name, trip['people'])))
        if trip_id not in article.data:
            article.data[trip_id] = trip_people
        else:
            article.data[trip_id + '1'] = trip_people
            n = 2
            while (trip_id + str(n)) in article.data:
                n = n + 1
            article.data[trip_id + str(n)] = article.data[trip_id]


#======================MAIN==========================


def cavepeep_linker_initialise(sender, context):
    context['trip_list'] = []



def cavepeep_linker_for_each_article(sender, context, article):
    if 'status' in article.metadata.keys() and article.metadata['status'] == ArticleStatus.DRAFT:
        return

    # If the article has the cavepeeps metadata
    if 'cavepeeps' in article.metadata.keys():
        # Parse metadata and return a list where each item contains a date,
        # cave, caver, and article reference
        trips = parse_metadata(article.metadata['cavepeeps'], article)
        article_link(context, article, trips)

        if article.status != ArticleStatus.UNLISTED:
            for trip in trips:
                context['trip_list'].append(trip)

    # If unlisted DO NOT ADD TO MAIN CAVEPEEPS dictionary.

def cavepeep_linker_final(sender, context, articles):
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