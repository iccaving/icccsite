from collections import namedtuple
import os
import logging
import re
import copy

def construct_bios(generator):
    settings=generator.settings
    readers=generator.readers
    contentpath=settings.get("PATH", "content")
    # There are files descirbing people/caves in the cave/caver directories
    # Look through cave/caver directory and process the markdown files therein
    # The outputted html is then saved along with the filename in a dictionary
    # which is added to the global context
    # The filename should match a name used in trip reports
    caverbios={}
    root=os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/cavers")))
    for dirpath, dirnames, filenames in os.walk(root):
        for afile in filenames:
            parsedfile=readers.read_file(dirpath, afile)
            content=parsedfile.content
            metadata=parsedfile.metadata
            # Create a tuple of the bio content and any metadata.
            # The metadata is made into a named tuple so its nicer
            # to access the items in it from the template
            caverbios[os.path.splitext(afile)[0]]=(content, namedtuple(
                'metadata', [x for x in metadata.keys()])(*[metadata[x] for x in metadata.keys()]))

    generator.context['caverbios']=caverbios
    logging.debug("Cavepeep: Caver bios assembled")

    cavebios={}
    root=os.path.realpath(
        os.path.abspath(os.path.join(contentpath + "/caves")))
    for dirpath, dirnames, filenames in os.walk(root):
        for afile in filenames:
            parsedfile=readers.read_file(dirpath, afile)
            content=parsedfile.content
            metadata=parsedfile.metadata
            cavebios[os.path.splitext(afile)[0]]=(content, metadata)

    generator.context['cavebios']=cavebios
    logging.debug("Cavepeep: Cave bios assembled")


def generate_cave_pages(generator, writer):
    # For every cave generate a page listing the articles that mention it
    row=namedtuple('row', 'filename cavebio cavemeta articles data')
    cavepages={}
    data={}
    cavebios=generator.context['cavebios']
    cavepeep_cave=generator.context['cavepeep_cave']
    template=generator.get_template('cavepages')

    # ==========Write the individual cave pages================
    for cave in cavepeep_cave:
        # If it was a through trip then the 'cave' string will be
        # 'cave1 > cave2' and we want the trip report link to appear on both
        # cave pages
        for entrance in cave.split('>'):
            entrance=entrance.strip()

            # Cave_peep cave is sorted by 'trip' so through trips count uniquely
            # Now we seperate them and so we must ensure that there are no
            # duplicate entries by using a dictionary
            if entrance not in cavepages.keys():
                cavebio=''
                cavemeta=''
                if entrance in cavebios:
                    # If a description is available for the cave retrieve it.
                    logging.debug("Bio generated for " + entrance)
                    cavebio=cavebios[entrance][0]
                    cavemeta=cavebios[entrance][1]

                    # Adds a 'map' entry to the dictionary that will be passed
                    # to the metainserter plugin. This places and embedded
                    # google map of the coords specified in the location
                    # metadata
                    if 'location' in cavemeta.keys():
                        data['map']="""<div class="padmore"><iframe width="100%" height="450" frameborder="0" style="border:0" allowfullscreen src="https://www.google.com/maps/embed/v1/search?q=""" + \
                            re.sub(r',\s*', "%2C", cavemeta['location'].strip(
                            )) + """&maptype=satellite&key=AIzaSyB03Nzox4roDjtKoddF9xFcYsvm4vi26ig" allowfullscreen></iframe></div>"""
                    else:
                        if 'map' in data.keys():
                            del data['map']

                filename='caves/' + str(entrance) + '.html'
                cavepages[entrance]=(row(filename, cavebio, cavemeta,
                                           cavepeep_cave[cave], copy.deepcopy(data)))
            else:
                # If the cave was added previously then we add just to the list
                # of articles it already has.
                cavepages[entrance].articles.extend(
                    cavepeep_cave[cave])

    for entrance, page in cavepages.items():
        writer.write_file(page.filename, template, generator.context,
                          cavename=entrance,
                          articles=sorted(
                              page.articles, key=lambda x: x.date, reverse=True),
                          bio=page.cavebio, meta=page.cavemeta, data=page.data)

    # ==========Write the index of caves================
    row=namedtuple('row', 'name number recentdate meta')
    # Refactor into useful format for index
    # Columns: Cave Name, Number of reports for that cave, the most recent
    # report date, the metadata for that cave
    caves=[row(x, len(cavepages[x].articles), max([y[1] for y in cavepages[x].articles]), cavebios[
                 x][1] if x in cavebios.keys() else None) for x in cavepages.keys()]
    template=generator.get_template('cavepage')
    filename='caves/index.html'

    writer.write_file(filename, template, generator.context,
                      caves=sorted(caves, key=lambda x: x.name))


def generate_person_pages(generator, writer):
    # For each person generate a page listing the caves they have been in and the article that
    # describes that trip
    authors={}
    caverbios=generator.context['caverbios']
    cavepeep_person=generator.context['cavepeep_person']

    for item in generator.authors:
        authors[item[0].name]=item[1]
    template=generator.get_template('personpages')
    for person in cavepeep_person:
        caverbio=''
        cavermeta=''
        authoredarticles=None
        if person in authors:
            authoredarticles=authors[person]
        # Check if they have a bio written about them
        if person in caverbios:
            logging.debug("Bio generated for " + person)
            caverbio=caverbios[person][0]
            cavermeta=caverbios[person][1]
        filename='cavers/' + person + '.html'
        writer.write_file(filename, template, generator.context, personname=person,
                          articles=sorted(
                              cavepeep_person[person], key=lambda x: x.date, reverse=True),
                          bio=caverbio, meta=cavermeta,
                          authoredarticles=authoredarticles)

    # ==========Write the index of cavers================

    template = generator.get_template('personpage')
    filename = 'cavers/index.html'
    row = namedtuple('row', 'name number recentdate meta')
    people = [row(name, len(cavepeep_person[name]), cavepeep_person[name][0].date, caverbios[name][1] if name in caverbios.keys() else None) for name in cavepeep_person.keys()]
    people = sorted(people, key=lambda tup: tup[2], reverse=True)
    writer.write_file(filename, template, generator.context, people=people)
    #[ (cave, article, date) ]
