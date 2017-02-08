This is the repository of the Imperial College Caving Club website. For build and deployment instructions please see the [wiki](https://github.com/iccavingrepo/icccsite/wiki)

<!--
#Contents
* [Basic set-up (linux)](#basic)
* [Writing Trip Reports (linux)](#write)
* [Set Up and Writing Trip Reports (windows)](#winduhs)
* [Advanced Setup; building the site and uploading](#advanced)
* [Advanced editing](#change)
* [Plugins](#plugins)
* [Tools](#tools)

Instructions are based on a linux set up but the semantic procedure (if not commands) should be the same. Scroll down for the Windows GUI version.

#<a id="basic"></a>Basic set up

Install git! Get yourself a github account. Add yourself (by logging into the iccaving github account) or get someone to add you as a contributer to https://github.com/iccavingrepo/.
Then set up the repo on your computer.

    git clone https://github.com/iccavingrepo/icccsite

Now make sure you've got a good text editor that allows you to select text encoding and line break encoding. For reference the site uses utf-8 and lf (unix) line breaks. This will save a lot of trouble later. For linux, the Gedit editor allows this. I use [atom](atom.io).

#<a id="write"></a>Writing Trip Reports
First pull the repo so you're up to date. Navigate to the directory then:

    git pull

Then add your write your trip report as a markdown file (.md extenstion) to the content/ folder. If its a standard post or trip report stick it in the content/articles/ folder. Try to keep to the placename-yyyy-mm-dd.md filename format where possible.

##File layout
There is a template.md file in the root of the repo. Copy and paste this and fill it according to the instructions within. If in doubt have a look at an existing article. Make sure to use your nice editor with utf-8 and lf line breaks.

The key points are:
* There is a set of metadata at the top of each file. Make sure to fill this out
* Below the metadata, write your report
* Markdown syntax is simple and available online. Look it up, or look at another article to format yours. [Also check this](https://help.github.com/articles/markdown-basics/)
* HTML works fine in markdown files (the same as they would in an html file) so if you can't do something with markdown just stick the html in.

##Metadata
All trip reports can have the following metadata:

*Title*: Title of the trip, i.e Wales III or Yorkshire IV or France

*Date*: Date in YYYY-MM-DD format

*Location*: Location of trip i.e Yorkshire, Wales, or France. This is mostly used to autogenerate the photoarchive directory and can be left blank if it doesnt seem useful.

*Summary*: The short blurb that will appear on the main page.

*Type*: Usually either 'trip' or 'tour' depending on the trip report type. 'stickyindex' for the main calender item on the index page or 'index' for announcements.

*Photoarchive*: Delete for no photo archive, leave blank for autogenerated location, or type a custom path for the archive (/photo_archive/newzealand/YYYY-MM-DD%20-%20Placename). You will have to make this folder and populate it yourself.

*Mainimg*: filename including extension of image in photoarchive folder to display in the article, leave blank for no image.

*Thumbl*: filename including extension of image in photoarchive folder to display as the left thumbnail on the main index page

*Thumbr*: same but the right thumbnail

*Authors*: The authors of the article, seperated by commas e.g. "Stores Gnomes, Stores Mice"

*Cavepeeps*: A list of the trips that happened. Normal trips and through trips supported. Format as below:

    DATE=YYYY-MM-DD; CAVE=Cave 1; PEOPLE=Person 1, Person 2, Person 3, Person 4;
    DATE=YYYY-MM-DD; CAVE=Cave 2 > Cave 3; PEOPLE=Person 1, Person 2, Person 3, Person 4;

Each entry should be on a new line and lines after the first 1 should be indented by more than 4 spaces (essetially match up the start of the entries).

*Oldurl*: If this is an old trip report being converted copy the caving url from /rcc/ e.g /rcc/caving/place/YYYY-MM-DD-place.php and write it here. Otherwise delete this.

*Status*: Set this to "draft" if you don't want it to appear on the site yet or delete entirely/set to "published" if you do or unlisted if you want the article to get published but not appear on the index, sidebar or archive page (accessible by direct link only essentially).

##Special pages/posts

###Announcments/info posts
Announcements (or info posts or whatever) on the main page with the type 'index' can also have the following metadata (in addition to the article metadata above):

*Link*: To set the a custom link from the announcement.

*Linktext*: What the link text should be.

These should be used to announce upcoming events or link to subsites etc. Anything that isn't really a trip or tour (links to articles on expedition subsites for example).

Also the content of the md file is used rather than the summary, to allow for easier long form content on the index page if so desired.

###Cave pages

The site generator generates a list of all the caves that are mentioned in the cavepeeps metadata of all the articles. It creates a page with a table listing all the trip reports mentioning that cave. It will also include an markdown/html blurb at the top if there is a markdown file in the caves/ directory with a filename matching the cavename. In that file the following metadata should be used:

*Country*: Country the cave is located in.

*Region*: The broad region, like Yorkshire or Andalucia.

*Subregion*: The valley, fell, town etc. where the cave is located. Like Leck Fell or Little Neath.

*System*: Cave system that the cave is part of. I've so far been using this as a "you might be able to do exchanges" type of signal. i.e easegill is seperate from the three counties system despite being connected underwater.

*Location*: The location of the cave in decimal degrees e.g "52.134534, -2.134532". Just get it off google.

Below the metadata you can write whatever you want in markdown/html and it will appear at the top of the cave's page, above the trip listings.

###People pages
Similar to the cave pages. There is no specific metadata here so write what you want.

##In page tags

###Articles

#####Main Image

There are a couple of tags/markdown shortcuts you can place in any article in addition to the standard markdown syntax.

If you have defined a mainimg in your article metadata then to position the mainimg in the page use:

    {{ mainimg }}

This will be replaced by all the lovely html for the image.

#####Lists of people

If you have defined a cave, date and people in cavepeeps then to position a list of all cavers mentioned, with links to their pages, use:

    {{ allpeople }}

I've been using:

    #####{{ allpeople }}

Which becomes header 5 as there is no styling by default on the list (other than being links).

Also you can easily print lists of people on a specific trip by copying and pasting what you wrote in the cavepeeps metadata! For example:

    {{ DATE=2016-01-01; CAVE=Jingling Pot; }}

Again, thats just a list of plain links so format it nicely:

    ###Cave Name: {{ DATE=2016-01-01; CAVE=Jingling Pot; }}

#####Inline Photos

There is a plugin active to allow easy inline posting of images. Similar to the way links work in standard markdown:

    {"Caption Goes Here Or Not" left}(filename.jpg)

Within the curly braces on the left there is a caption in quotes, this is optional. There is also an alignment (left) on the right which can be left/right/center. In the round braces on the right is the url in quotes of the image. This will link to photos in the specified photoarchive (i.e just use the filename!). Also the link ('href' attribute of 'a' tag) will (cleverly) point at the curator html page for that photo. To point it somewhere else:

    {"Caption Goes Here Or Not" left}(filename.jpg, http://some.link/elsewhere)

If you want to link to images outside of the photoarchive then put an exclamation mark after the first curly brace:

    {!"Caption Goes Here Or Not" left}(www.external.com/image.jpg)

Both the img src and a href will point to the image. If you want the 'a' tag 'href' (image link) to point somewhere else:

    {!"Caption Goes Here Or Not" left}(www.external.com/image.jpg, http://some.link/elsewhere)

###Cave pages

The cave pages currently have 1 tag you can use:

    {{ map }}

If you have specified the location metadata then this will insert a Google Maps embed centered on the cave.

##Finishing
Save your .md file. Track the file in git:

    git add path/to/file

Commit your file(s):

    git commit -m "Put descriptive message here"

Please put in a good descirption of what you have done. E.g "Added a trip report for Yorkshire 3 15/03/15".
Finally push your changes:

    git push

And that can be it. Contact whoever is in charge of the site to let them know to update it. If you want to see it yourself (good to check for formatting errors) then you can run the test script:

    sh test.sh

This will generate the site "locally". Change to the output directory and start the webserver of your choice. I suggest:

    python3 -m http.server

Navigate to 0.0.0.0:8000 with your web browser to see it. It is likely that images won't show up.

#<a id="winduhs"></a>Windows GUI set up
Shit, that looks well hard. What's a poor Windows user to do? If you prefer clicking to typing, read on.

Get yourself a [github](https://github.com/) account. Then install [Github for Windows](https://desktop.github.com/). Get someone else to add you to the repo. When you launch GitHub, click the + in the top left, then choose iccavingrepo->icccsite. Github will ask you where to download the repo to - I suggest My Documents. It will download all the files. To make a new trip report, copy template.md to the appropriate folder and then rename to something sensible like yorkshire-2015-09-02.md

You can then edit them using [MarkdownPad](https://markdownpad.com/download.html). This is cute cos it shows what the text will look like on the right hand page, which is useful for spotting obvious mistakes.

Once you're happy with your trip report, you can commit your change - go to Github, and it should have '1 uncommitted change' in the top bar. Click there, enter a description of your commit, click commit to master, then click sync in the top right.

Building and synchronising the website on Windows is not as straightforwards - if you are capable of doing it, then you're unlikely to be reading this section. The advice for linux below applies.

#<a id="advanced"></a>Advanced Set Up
If you want to be able to build and deploy the site yourself look here, otherwise ignore.
##Installing Pelican
First make sure you have python 3. Python 2 will not work, it doesn't do unicode easily so I can't be bothered with it. If you like you can install virtualenv and then everything is set up in the env/ folder. You can then also use the publish.sh script. Otherwise:

Pelican is a python based static site generator. Install it:

    pip install pelican

Note that `python -m pip install pelican` might be necessary depending on your `PATH`.

Install the Markdown package as that is what the trip reports should be written in:

    pip install Markdown

Install BeautifulSoup:

    pip install beautifulsoup4

Firstly run:

    pelican content -s publishconf.py

This will build the site and output it to the output folder. To push the site to the union server (and therefore make it live) you will need at least sftp access (can be requested via a sysadmin form). You need to get the contents of the output folder into the /home/www/htdocs/rcc/caving/ folder. If you have ssh access (requested by emailing the sysadmin) then you can run:

    rsync -avz -e "ssh -p 10022" --chmod=ug+rwx,o-wx,o+r output/ username@dougal.union.ic.ac.uk:/home/www/htdocs/rcc/caving

The 'avz' are archive (push the files with all their attributes), verbose (tell us what's going on), and compress (make it smaller for transfer) respectively. The "ssh -p 10022" is an alternative port that gets round the IC vpn. If you have access to the vpn then you can log into that and omit that bit of the command. --chmod.... sets the permissons correctly.

Note that the easiest way to do this on Windows involves Cygwin, and so is not easy by any stretch of the imagination.

###Virtual environments are your friend
Don't mess up your beautiful clean python install by installing all of that ^ crap. Just use the virtualenv helpfully placed in the repo for you.

To switch to it and get python3, pelican, markdown, bs4 etc on your path:

     source env/bin/activate

Now building the site should just work. And to get out of the virtualenv:

     deactivate

Don't pip install or anything like that while in the virtualenv unless you know what you're doing.


##Photos
The photos are a bit more complicated. To do this you will need at least SFTP access.
* Make folder in appropriate location in photo_archive. e.g "/home/www/htdocs/rcc/caving/photo_archive/region/YYYY-MM-DD%20-%20Placename". Note: %20 is just a space character. Your sftp client can probably handle spaces.
* Upload photos to this folder.
* Run the thumb.sh script that is in photo_archive root from the directory with your new photos. This will generate the thumbnails and small images.
* Run the curator.sh script that is in photo_archive root from the directory with your new photos.
* In the relevant article, fill out the relevent metadata. (This can be done before making the folder/uploading photos, the links will just be dead until you do)
Done.

#<a id="change"></a>Changing other parts of the site
Hello awful cavers of the future. So you're sick of the shade of grey I chose for the sidebar? Or you've decided that freshers don't need an FAQ link in the sidebar, they need a gif of some genitals? Well against my better judgement this section is for you.

If it's not the content of a trip report or a page you're trying to change (you can't find it in the md files in articles/ or it appears everywhere, like the header or sidebar) then it's likely its part of the theme of the site. Navigate to 'themes/ICTheme/'. There's two subfolders. "Static" contains the css and javascript files. Templates contains other stuff.

##CSS
You can change an awful lot of the website just from the CSS. All of the styling stuff is here (colours, fonts, text sizes, layout). I've used the SASS css preprocessor to enable things like variables and nested css selectors which is very handy. So to edit this you should install SASS. Then edit the main.scss file or the mobile.scss file, run sass on it to generate the css file and build the website as normal.

At the moment there are some media queries to change the site for smaller screens and they are included in the main.scss file but when the screen size drops below a certain threshold it loads the mobile.scss file in addition which overrides lots of things. I did this because the mobile site is quite different and it seemed tidier.

##javascript
There's a couple of JS libraries in use. Jquery, which I don't think anyone using javascript could without. sorttable allows for sortable tables. There's a little readme in the file itself. There's also a cookie library which was mainly used on a custom photo gallery page. There is a small js html5 chart generating library called chartjs as well.

There are a few small js scripts in header.js. Mostly they make minor changes to the layout of the pages. But there's also one that controls the opening/closing of the sidebar.

The sidebar.js contains quite a large js script that animates the drawer effect of the the sidebar items.

##Templates
The entire site is based on templates. They use a templating language called Jinja. After reading all of the articles and pages in the website looks at the templates to see how you want the information displayed. Most of them (articles/pages templates) are very much just structural, telling Pelican where to put the information from the articles/pages and containing no content themselves. The main exception to this is the sidebar. The sidebar templates is in the includes/ subdirectory and contains quite a lot of non-autogenerated content. So its a good place to look to change things.

The base template is essentially stuff that gets included in every other template (you can inherit from other templates). The site <head> tag is here for example.

#Plugins<a id="plugins"></a>
Its possible to write plug ins for pelican that allow you do some pretty awesome things. Here I will document the plug ins active on the IC site.

##Subsites
There is a plugin that allows subs sites to be added easily (like the NZ or Slov sites). They are treated essentially entirely seperate from the main site so you can have different plugins and completely different themes. Though its probably best just to modfiy the colour scheme slightly :P.
###Set up
It works like the main site. There is a content folder to put articles in, a plug in folder for site specific plugins, a themes folder for a site specific theme. The settings file is a little different. It has to be called "settings.py" and reside in the root of the subsite.

In "settings.py" there are two mandatory settings:

    PATH = 'content'

This should point to the folder that your markdown files are in.

    SUBSITE_PATH = 'newzealand'

This should be the name of the subdirectory you want the site to reside in once its published.

All other settings are optional and will default to the main site's settings. All of the file paths in this settings file will be relative to the file itself (i.e not the main site root). Useful settings to change might be the THEME, PLUGINS, PLUGIN_PATHS or STATIC_PATHS which will copy directories in the subsites content folder into the subsites output (just like for the main site).

##Metainserter

It finds Jinja-style tags of the format "{{ example }}" in a page and replaces them with something specified in the metadata tag (if you've used jinja or some other templating language then it's the same as that). The metadata tag is a script tag on each article with the ID of "metadata". It expects this to contains a single javascript object (which functions like a dictionary). The metadata object's keys will (if they are encased in the double curly braces) be replaced with the value paired to that key (sans curly braces). For example if the whole tag on the page looked like this:

    <script style="display: none;" id="metadata" type="application/json">
      {"cave":"easegill"}
    </script>

Then anywhere in the article the string "{{ cave }}" will be replaced with "easegill". The metadata script tag is placed in the html according to the page's template by some Jinja tags that look like this:

    <script style="display: none;" id="metadata" type="application/json">
      {
      {% for key in article.data %}
      {% if loop.index > 1 %},{% endif %}
      """{{ key }}""":"""{{ article.data[key] }}"""
      {% endfor %}
      }
    </script>

Currently this is included in the article and cave templates. Meaning that metainserter only works on those page types. To get metainserter working on another page type should be as simple as dropping exactly that tag into the page's template and also adding it in the obvious place in "metainserter.py" (literally a comment that says "this is the obvious place").

You might be able to see how the metadata is added by looking at the jinja code above. Essentially another plugin has already added it to the articles metadata, specifically to "data" in the metadata dictionary. For example in the cavepeeps plugin:

    try:
        article.data["allpeople"] = outallpeople
    except:
        article.data = {}
        article.data["allpeople"] = outallpeople

For each article we have generated a string containing a list of people who went on that trip called "outallpeople". We add it to "article.data" which is just a dictionary. The key is the string we want to replace and the value is the string we'll replace it with. In this case "{{ allpeople }}" will be replaced with whatever the string "outallpeople" resolves to (a list of names).

Any other plugin can do this. Just add to the "data" dictonary in an article object and metainserter will do the rest.


#Tools<a id="tools"></a>

##meta_replacer.py

Tool that will run through the metadata of any articles below a specififed directory and do substitutions on that meta data. Good for, fixing peoples names in the past without actually digging through all the articles or maybe you've spelt someones name wrong 4 trips in a row.

    python meta_replacer.py path/to/articles/ --meta <metadatasection> --pattern <what do you want replaced> --sub <replace with> --start <earliest articles to consider> --end <latest articles to consider>

The start and end dates are in the format YYYY-MM-DD and are optional, not specifying them will result in all articles being looked at. Example usage:

    python meta_replacer.py content/trips/ --meta Cavepeeps --pattern "An VDP" --sub "Anne VDP"

The script will offer to list the affected articles and affected lines in those articles before it does any replacing so don't worry about experimenting (also git will save you probably).
-->
