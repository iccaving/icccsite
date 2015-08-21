from pelican import signals, utils
from collections import namedtuple, defaultdict, OrderedDict
import os
from datetime import date
import pytz


def cavepeeplinker(generator):
    # Create array of people, caves they have been to and the articles that the trip is recorded in
    # Also create array of caves and the articles that refer to the cave (could have a 'people who have been in this
    # cave' thing as well but I didn't think it was useful

    cavepeep = []  # Set up list to hold named tuples
    row = namedtuple('row', 'cave person article')

    for article in generator.articles:  # Loop through articles
        # If the article has the cavepeeps metadata
        if 'cavepeeps' in article.metadata.keys():
            # Seperate the value of cavepeeps into a list of characters
            string = list(article.cavepeeps)
            inbracks = False
            cave = ""
            person = ""
            for char in string:
                # Essentially this checks when we should start writing people
                # names rather than caves names
                if char == "(":
                    inbracks = True

                # Checks when we should stop writing people names and start a
                # new cave name
                elif char == ")":
                    cave.strip(' \t\n\r')
                    person.strip(' \t\n\r')
                    cavepeep.append(row(cave, person, article))
                    inbracks = False
                    cave = ""
                    person = ""

                elif char == ",":  # Start writing a new people name
                    cave.strip()
                    person.strip()
                    cavepeep.append(row(cave, person, article))
                    person = ""

                else:
                    if inbracks == True:  # Write people name
                        person += char
                        # Hacky way to remove leading whitespace. Strip didnt
                        # seem to work (?)
                        if person == ' ':
                            person = ''
                    elif inbracks == False:  # Write cave name
                        cave += char
                        if cave == ' ':
                            cave = ''

    cavepeep.sort(key=lambda tup: tup.person)  # Sort the list by person name
    cavepeep_person = OrderedDict()
    # Add the entries to an ordered dictionary so that for each person (the key) there is a list of tuples
    # containing the cavename and the article its mentioned in
    for item in cavepeep:
        cavepeep_person.setdefault(item.person, []).append(
            (item.cave, item.article))

    # Find the most recent article's date
    for person in cavepeep_person:
        maxdate = utils.SafeDatetime(
            year=1900, month=1, day=1, tzinfo=pytz.timezone('Europe/London'))
        for tup in cavepeep_person[person]:
            if maxdate < tup[1].date:
                maxdate = tup[1].date
        # For each person now the dictionary will give a tuple containg a list (of tuples) of the article
        # and cave name, and the most recent article
        cavepeep_person[person] = (cavepeep_person[person], maxdate)

    print "Cavepeeps: cavepeep_person assembled"

    cavepeep.sort(key=lambda tup: tup.cave)  # Sort the list by cave name
    flag = False
    cavepeep_cave = OrderedDict()
    # Add the entries to an ordered dictionary so that for each cave (the key) there is a list
    # containing articles its mentioned in. As two people can mention the same cave in the same
    # article there is also duplicate checking so that the same article is not linked twice for
    # cave
    for item in cavepeep:
        if item.cave in cavepeep_cave:
            for art in cavepeep_cave[item.cave]:
                if item.article == art:
                    print "Cavepeep: Duplicate reference to article from same cave"
                    flag = True
        if flag == False:
            cavepeep_cave.setdefault(item.cave, []).append((item.article))
        else:
            flag = False

    # Find the most recent article's date
    for cave in cavepeep_cave:
        maxdate = utils.SafeDatetime(
            year=1900, month=1, day=1, tzinfo=pytz.timezone('Europe/London'))
        for art in cavepeep_cave[cave]:
            if maxdate < art.date:
                maxdate = art.date
        # For each person now the dictionary will give a tuple containg a list (of tuples) of the article
        # and cave name, and the most recent article
        cavepeep_cave[cave] = (cavepeep_cave[cave], maxdate)

    print "Cavepeeps: cavepeep_cave assembled"

    # Add the dictionaries to the global context (makes them accessible to
    # other plugins and the templates)
    generator.context['cavepeep_cave'] = cavepeep_cave
    generator.context['cavepeep_person'] = cavepeep_person

    print "Cavepeeps: Success!"


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
            caverbios[os.path.splitext(afile)[0]] = readers.read_file(
                dirpath, afile).content
    generator.context['caverbios'] = caverbios

    cavebios = {}
    root = os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/caves")))
    for dirpath, dirnames, filenames in os.walk(root):
        for afile in filenames:
            cavebios[os.path.splitext(afile)[0]] = readers.read_file(
                dirpath, afile).content
    generator.context['cavebios'] = cavebios


def generatecavepages(generator, writer):
    # For every cave generate a page listing the articles that mention it
    template = generator.get_template('cavepages')
    for cave in generator.context['cavepeep_cave']:
        cavebio = ''
        if cave in generator.context['cavebios']:
            # If a description is available for the cave retrieve it.
            print "Bio generated for " + cave
            cavebio = generator.context['cavebios'][cave]
        filename = 'caves/' + str(cave) + '.html'
        writer.write_file(filename, template, generator.context, cavename=cave,
                          reports=generator.context['cavepeep_cave'][cave][0], bio=cavebio)


def generatecavepage(generator, writer):
    # Generate a page linking to all the cave pages
    template = generator.get_template('cavepage')
    filename = 'caves/index.html'
    writer.write_file(filename, template, generator.context)


def generatepersonpages(generator, writer):
    # For each person generate a page listing the caves they have been in and the article that
    # describes that trip
    template = generator.get_template('personpages')
    for person in generator.context['cavepeep_person']:
        caverbio = ''
        if person in generator.context['caverbios']:
            print "Bio generated for " + person
            caverbio = generator.context['caverbios'][person]
        filename = 'cavers/' + str(person) + '.html'
        writer.write_file(filename, template, generator.context, personname=person,
                          reports=generator.context['cavepeep_person'][person][0], bio=caverbio)


def generatepersonpage(generator, writer):
    # Create a page listing all the people pages
    template = generator.get_template('personpage')
    filename = 'cavers/index.html'
    writer.write_file(filename, template, generator.context)


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
