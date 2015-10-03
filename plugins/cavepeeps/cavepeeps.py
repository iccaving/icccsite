from pelican import signals, utils
from collections import namedtuple, defaultdict, OrderedDict
import os
from datetime import date, datetime
import logging
import string
import sys


def parse_metadata(metadata, article):
    # Create array of people, caves they have been to and the articles that the
    # trip is recorded in. Also create array of caves and the articles that
    # refer to the cave (could have a 'people who have been in this cave' thing
    # as well but I didn't think it was useful
    cavepeep = []  # Set up list to hold named tuples
    row = namedtuple('row', 'date cave person article')
    # Ensure the metadata is a list. It will be a string if there is
    # just one entry
    if type(metadata) is not list:
        art_metadata = [metadata]
    else:
        art_metadata = metadata
    # Look at all the entries. Each will describe a trip that happened
    # on a date.
    for entry in art_metadata:
        item_date = None
        item_caves = None
        item_people = None
        # Split each entru by semicolons
        entry = entry.split(';')
        for item in entry:
            # Remove trailing and leading whitespace and if its blank
            # ignore
            item = item.strip()
            if item == '':
                continue
            # Find out type of item we are looking at
            try:
                item_type, item_values = item.split('=')
            except ValueError:
                logging.critical("Error with the cavepeep metadata. Check that there are semicolons between DATE=, CAVE=, PEOPLE= (not colons) and that there are equals after each.")
                logging.critical(str(article.title) + ' ' + str(article.date.strftime('%Y-%m-%d')))
                sys.exit()
            if item_type == 'DATE':
                item_date = datetime.strptime(item_values, '%Y-%m-%d')
            elif item_type == 'CAVE':
                # Ensure the cave or caves are in a list. This will
                # normally be just cavename or
                # Entrancecave > Exitcave but in fact should work for
                # an arbitrary sequence of cave names.
                item_caves = item_values.split('>')
                item_caves = item_caves if type(
                    item_caves) is list else [item_caves]
                item_caves = [x.strip() for x in item_caves]
            elif item_type == 'PEOPLE':
                # Ensure the people are in a list
                item_people = item_values.split(',')
                item_people = item_people if type(
                    item_people) is list else [item_people]
                item_people = [x.strip() for x in item_people]

        if item_date is not None and item_caves is not None and item_people is not None:
            # If we have all the required data then append it to the
            # big list. Each entry has one date so no need to loop over it
            for cave in item_caves:
                for person in item_people:
                    cavepeep.append(
                        row(item_date, cave, person, article))
        else:
            logging.critical("Error with the cavepeep metadata. Are DATE, PEOPLE, CAVE present and spelt correctly? If there's no cavepeep data please delete the row from the metadata.")
            logging.critical(str(article.title) + ' ' + str(article.date.strftime('%Y-%m-%d')))
            sys.exit()
    return cavepeep


def articlelink(peoplelist, article, generator):
    # Function to link articles with lists of people that relate to the trips
    # in that article
    peopletrips = {}
    allpeople = set()
    for item in peoplelist:
        fullname = item.person
        tripid = item.date.strftime('%Y-%m-%d') + '-' + item.cave.translate(
            {ord(c): None for c in string.punctuation}).replace(' ', '-')
        if tripid in peopletrips.keys():
            peopletrips[tripid].append(fullname)
        else:
            peopletrips[tripid] = [fullname]
        allpeople.add(fullname)

    # Make the metadata available to the article template
    # article.peopletrips = article.metadata["peopletrips"] = peopletrips
    # article.allpeople = article.metadata["allpeople"] = [val for key, val in allpeople.items()]

    # The metadata might need to be used to replace a tag in the article
    # so add it to the metadata item that will be available to metainserter
    outallpeople = ''
    for index, person in enumerate(allpeople):
        if index > 0:
            outallpeople += ', '
        outallpeople += """<a href='""" + generator.settings["SITEURL"] + """/cavers/""" + person.replace(" ", "%20") + """.html'>""" + person + """</a>"""
    outpeopletrips = {}
    for key in peopletrips:
        outpeopletrips[key] = ''
        for index, person in enumerate(peopletrips[key]):
            if index > 0:
                outpeopletrips[key] += ', '
            outpeopletrips[key] += """<a href='""" + generator.settings["SITEURL"] + """/cavers/""" + person.replace(" ", "%20") + """.html'>""" + person + """</a>"""

    try:
        article.data["allpeople"] = outallpeople
        for key in outpeopletrips:
            article.data[key] = outpeopletrips[key]
    except:
        article.data = {}
        article.data["allpeople"] = outallpeople
        for key in outpeopletrips:
            article.data[key] = outpeopletrips[key]

def cavepeeplinker(generator):
    cavepeep = []
    for article in generator.articles:  # Loop through articles
        # If the article has the cavepeeps metadata
        if 'cavepeeps' in article.metadata.keys():
            # Parse metadata and return a list where each item contains a date,
            # cave, caver, and article reference
            cavepeep_partial = parse_metadata(
                article.metadata['cavepeeps'], article)
            articlelink(cavepeep_partial, article, generator)
            cavepeep += cavepeep_partial
    cavepeep.sort(key=lambda tup: tup.person)  # Sort the list by person name
    cavepeep_person = OrderedDict()
    # Add the entries to an ordered dictionary so that for each person
    # (the key) there is a list of tuples containing the cavename, the article
    # its mentioned in, and the specific date of the cave visit
    row = namedtuple('row', 'cave article date')
    for item in cavepeep:
        cavepeep_person.setdefault(item.person, []).append(
            row(item.cave, item.article, item.date))

    # Find the most recent visit date
    for person in cavepeep_person:
        maxdate = datetime.strptime('1900-01-01', '%Y-%m-%d')
        for tup in cavepeep_person[person]:
            if maxdate < tup[2]:
                maxdate = tup[2]
        # For each person now the dictionary will give a tuple containg a list (of tuples) of the article,
        # date, cave name, and the most recent article
        cavepeep_person[person] = (cavepeep_person[person], maxdate)

    logging.debug("Cavepeeps: cavepeep_person assembled")

    cavepeep.sort(key=lambda tup: tup.cave)  # Sort the list by cave name
    flag = False
    cavepeep_cave = OrderedDict()
    # Add the entries to an ordered dictionary so that for each cave (the key) there is a list
    # containing articles its mentioned in. As two people can mention the same cave in the same
    # article there is also duplicate checking so that the same article is not linked twice for
    # cave
    row = namedtuple('row', 'article date')
    for item in cavepeep:
        if item.cave in cavepeep_cave:
            for art, date in cavepeep_cave[item.cave]:
                if item.article == art and item.date == date:
                    logging.debug(
                        "Cavepeep: Duplicate reference to article from same cave: " + item.cave)
                    flag = True
        if flag is False:
            cavepeep_cave.setdefault(item.cave, []).append(
                row(item.article, item.date))
        else:
            flag = False

    # Find the most recent article's date
    for cave in cavepeep_cave:
        maxdate = datetime.strptime('1900-01-01', '%Y-%m-%d')
        for art, date in cavepeep_cave[cave]:
            if maxdate < date:
                maxdate = date
        # For each person now the dictionary will give a tuple containg a list (of tuples) of the article,
        # cave name and date, and the most recent article
        cavepeep_cave[cave] = (cavepeep_cave[cave], maxdate)

    logging.debug("Cavepeeps: cavepeep_cave assembled")

    # Add the dictionaries to the global context (makes them accessible to
    # other plugins and the templates)
    generator.context['cavepeep_cave'] = cavepeep_cave
    generator.context['cavepeep_person'] = cavepeep_person

    logging.debug("Cavepeeps: Success!")


def constructbios(generator):
    settings = generator.settings
    readers = generator.readers
    contentpath = settings.get("PATH", "content")
    # There are files descirbing people/caves in the cave/caver directories
    # Look through cave/caver directory and process the markdown files therein
    # The outputted html is then saved along with the filename in a dictionary
    # which is added to the global context
    # The filename should match a name used in trip reports
    caverbios = {}
    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/cavers")))
    for dirpath, dirnames, filenames in os.walk(root):
        for afile in filenames:
            content = readers.read_file(dirpath, afile).content
            metadata = readers.read_file(dirpath, afile).metadata
            # Create a tuple of the bio content and any metadata.
            # The metadata is made into a named tuple so its nicer
            # to access the items in it from the template
            caverbios[os.path.splitext(afile)[0]] = (content, namedtuple(
                'metadata', [x for x in metadata.keys()])(*[metadata[x] for x in metadata.keys()]))
    generator.context['caverbios'] = caverbios
    logging.debug("Cavepeep: Caver bios assembled")

    cavebios = {}
    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/caves")))
    for dirpath, dirnames, filenames in os.walk(root):
        for afile in filenames:
            content = readers.read_file(dirpath, afile).content
            metadata = readers.read_file(dirpath, afile).metadata
            cavebios[os.path.splitext(afile)[0]] = (content, namedtuple(
                'metadata', [x for x in metadata.keys()])(*[metadata[x] for x in metadata.keys()]))
    generator.context['cavebios'] = cavebios
    logging.debug("Cavepeep: Cave bios assembled")


def generatecavepages(generator, writer):
    # For every cave generate a page listing the articles that mention it
    template = generator.get_template('cavepages')
    for cave in generator.context['cavepeep_cave']:
        cavebio = ''
        cavemeta = ''
        if cave in generator.context['cavebios']:
            # If a description is available for the cave retrieve it.
            logging.debug("Bio generated for " + cave)
            cavebio = generator.context['cavebios'][cave][0]
            cavemeta = generator.context['cavebios'][cave][1]
        filename = 'caves/' + str(cave) + '.html'
        writer.write_file(filename, template, generator.context, cavename=cave,
                          articles=generator.context['cavepeep_cave'][cave][0], bio=cavebio, meta=cavemeta)
        # cavepeep(cave) = ([(article, date)], maxdate)


def generatecavepage(generator, writer):
    # Generate a page linking to all the cave pages
    template = generator.get_template('cavepage')
    cavebios = generator.context['cavebios']
    cavepeep_cave = generator.context['cavepeep_cave']
    filename = 'caves/index.html'
    # Make a nice data strcuture for the template to access
    row = namedtuple('row', 'name number recentdate meta')
    caves = [row(x, len(cavepeep_cave[x][0]), cavepeep_cave[x][1], cavebios[x][
        1] if x in cavebios.keys() else None) for x in cavepeep_cave.keys()]
    writer.write_file(filename, template, generator.context, caves=caves)


def generatepersonpages(generator, writer):
    # For each person generate a page listing the caves they have been in and the article that
    # describes that trip
    authors = {}
    for item in generator.authors:
        authors[item[0].name] = item[1]
    template = generator.get_template('personpages')
    for person in generator.context['cavepeep_person']:
        caverbio = ''
        cavermeta = ''
        authoredarticles = None
        if person in authors:
            authoredarticles = authors[person]
        # Check if they have a bio written about them
        if person in generator.context['caverbios']:
            logging.debug("Bio generated for " + person)
            caverbio = generator.context['caverbios'][person][0]
            cavermeta = generator.context['caverbios'][person][1]
        filename = 'cavers/' + person + '.html'
        writer.write_file(filename, template, generator.context, personname=person,
                          articles=generator.context['cavepeep_person'][person][0], bio=caverbio, meta=cavermeta, authoredarticles=authoredarticles)


def generatepersonpage(generator, writer):
    # Create a page listing all the people pages
    template = generator.get_template('personpage')
    filename = 'cavers/index.html'
    caverbios = generator.context['caverbios']
    cavepeep_person = generator.context['cavepeep_person']
    row = namedtuple('row', 'name number recentdate meta')
    people = [row(x, len(cavepeep_person[x][0]), cavepeep_person[x][1], caverbios[x][
        1] if x in caverbios.keys() else None) for x in cavepeep_person.keys()]
    people = sorted(people, key=lambda tup: tup[2], reverse=True)
    writer.write_file(filename, template, generator.context, people=people)
    # ([ (cave, article, date) ], maxdate)


def register():
    # Registers the various functions to run during particar Pelican processes
    # Run after the article list has been generated
    signals.article_generator_finalized.connect(cavepeeplinker)
    signals.article_generator_finalized.connect(constructbios)
    # Run after the articles have been written
    signals.article_writer_finalized.connect(generatecavepages)
    signals.article_writer_finalized.connect(generatecavepage)
    signals.article_writer_finalized.connect(generatepersonpages)
    signals.article_writer_finalized.connect(generatepersonpage)
