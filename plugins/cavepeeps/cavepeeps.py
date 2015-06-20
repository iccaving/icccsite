from pelican import signals
from collections import namedtuple, defaultdict, OrderedDict
import os

def cavepeeplinker(generator):
  #Create array of people, caves they have been to and the articles that the trip is recorded in
  #Also create array of caves and the articles that refer to the cave (could have a 'people who have been in this
  #cave' thing as well but I didn't think it was useful

  cavepeep = [] #Set up list to hold named tuples
  row = namedtuple('row', 'cave person article')

  for article in generator.articles: #Loop through articles
    if 'cavepeeps' in article.metadata.keys(): #If the article has the cavepeeps metadata
      string = list(article.cavepeeps) #Seperate the value of cavepeeps into a list of characters
      inbracks = False
      cave = ""
      person = ""
      for char in string:
        if char == "(": #Essentially this checks when we should start writing people names rather than caves names
          inbracks = True

        elif char == ")": #Checks when we should stop writing people names and start a new cave name
          cave.strip(' \t\n\r')
          person.strip(' \t\n\r')
          cavepeep.append(row(cave, person, article))
          inbracks = False
          cave = ""
          person = ""

        elif char == ",": #Start writing a new people name
          cave.strip()
          person.strip()
          cavepeep.append(row(cave, person, article))
          person = ""

        else:
          if inbracks == True: #Write people name
            person += char
            if person == ' ': #Hacky way to remove leading whitespace. Strip didnt seem to work (?)
              person = ''
          elif inbracks == False: #Write cave name
              cave += char
              if cave == ' ':
                cave = ''

  cavepeep.sort(key=lambda tup: tup.person) #Sort the list by person name
  cavepeep_person = OrderedDict()
  #Add the entries to an ordered dictionary so that for each person (the key) there is a list of tuples
  #containing the cavename and the article its mentioned in
  for item in cavepeep:
    cavepeep_person.setdefault(item.person,[]).append((item.cave, item.article))

  print "Cavepeeps: cavepeep_person assembled"

  cavepeep.sort(key=lambda tup: tup.cave) #Sort the list by cave name
  flag=False
  cavepeep_cave = OrderedDict()
  #Add the entries to an ordered dictionary so that for each cave (the key) there is a list
  #containing articles its mentioned in. As two people can mention the same cave in the same
  #article there is also duplicate checking so that the same article is not linked twice for
  #cave
  for item in cavepeep:
    if item.cave in cavepeep_cave:
      for art in cavepeep_cave[item.cave]:
        if item.article == art:
          print "Cavepeep: Duplicate reference to article from same cave"
          flag=True
    if flag == False:
      cavepeep_cave.setdefault(item.cave,[]).append((item.article))
    else:
      flag = False

  print "Cavepeeps: cavepeep_cave assembled"

  #Add the dictionaries to the global context (makes them accessible to other plugins and the templates)
  generator.context['cavepeep_cave'] = cavepeep_cave
  generator.context['cavepeep_person'] = cavepeep_person

  print "Cavepeeps: Success!"

def generatecavepages(generator, writer):
  #For every cave generate a page listing the articles that mention it
  template = generator.get_template('cavepages')
  for cave in generator.context['cavepeep_cave']:
    filename = 'caves/' + str(cave) + '.html'
    writer.write_file(filename, template, generator.context, cavename=cave, reports=generator.context['cavepeep_cave'][cave])

def generatecavepage(generator, writer):
  #Generate a page linking to all the cave pages
  template = generator.get_template('cavepage')
  filename = 'caves/caves.html'
  writer.write_file(filename, template, generator.context)

def generatepersonpages(generator, writer):
  #For each person generate a page listing the caves they have been in and the article that
  #describes that trip
  template = generator.get_template('personpages')
  for person in generator.context['cavepeep_person']:
    filename = 'cavers/' + str(person) + '.html'
    writer.write_file(filename, template, generator.context, personname=person, reports=generator.context['cavepeep_person'][person])

def generatepersonpage(generator, writer):
  #Create a page listing all the people pages
  template = generator.get_template('personpage')
  filename = 'cavers/cavers.html'
  writer.write_file(filename, template, generator.context)

def register():
  #Registers the various functions to run during particar Pelican processes
  #Run after the article list has been generated
  signals.article_generator_finalized.connect(cavepeeplinker)
  #Run after the articles have been written
  signals.article_writer_finalized.connect(generatecavepages)
  signals.article_writer_finalized.connect(generatecavepage)
  signals.article_writer_finalized.connect(generatepersonpages)
  signals.article_writer_finalized.connect(generatepersonpage)
