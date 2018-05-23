from datetime import date, datetime
import re
from olm.logger import get_logger

logger = get_logger('olm.plugins.cavepeep')

def parse_metadata(metadata, article=None):
    trips = []

    # Ensure the metadata is a list. It will be a string if there is
    # just one entry
    title            = article.title if article else ""
    date             = article.date if article else datetime.now()
    cavepeeps        = [metadata] if not isinstance(metadata, list) else metadata

    # Look at all the entries. Each will describe a trip that happened
    # on a date.
    c = re.compile(r"""\s*DATE=\s*(\d\d\d\d-\d\d-\d\d)\s*;\s*CAVE=\s*([\s\w\D][^;]*)\s*;\s*PEOPLE=\s*([\s\w\D][^;]*);*[\n\t\r]*""")
    c2 = re.compile(r"""\s*NOCAVE=\s*([\s\w\D][^;]*);*[\n\t\r]*""")
    for entry in cavepeeps:
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
            item_date=date
            item_caves=None
            item_people=m2.group(1).split(',')
        else:
            logger.error(
                        "\nCavepeep metdata error in article: " + title + " " + str(date.strftime('%Y-%m-%d')) +
                "\nLine: " + entry +
                "\nAre DATE, PEOPLE, CAVE present and spelt correctly? Are there semicolons (not colons) seperating each section?" +
                "\nIf there's no cavepeep data please delete the row from the metadata.")
            continue
        
        item_caves_raw = "" if item_caves is None else item_caves
        item_caves = [] if item_caves is None else item_caves.split('>')
        item_caves = item_caves if type(item_caves) is list else [item_caves]
        item_caves = [x.strip() for x in item_caves ]

        item_people = item_people if type(item_people) is list else [item_people]
        item_people = [x.strip() for x in item_people]
        
        trip = {
            "article":   article, 
            "date":      item_date, 
            "caves":     item_caves,
            "caves_raw": item_caves_raw,
            "people":    item_people
        }

        trips.append(trip)
    
    return trips