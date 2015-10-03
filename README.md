Instructions are based on a linux set up but the semantic procedure (if not commands) should be the same.

#Basic set up

Install git! Get yourself a github account. Add yourself (by logging into the iccaving github account) or get someone to add you as a contributer to https://github.com/iccavingrepo/.
Then set up the repo on your computer.

    git clone https://github.com/iccavingrepo/nzsite.git

#Writing Trip Reports
First pull the repo so you're up to date. Navigate to the directory then:

    git pull

Then add your write your trip report as a markdown file (.md extenstion) to the nzsite/content/ folder. If its a standard post or trip report stick it in the nzsite/content/articles/ folder. Try to keep to the yyyy-mm-dd-placename.md filename format where possible.

##File layout
There is a template.md file in the root of the nzsite repo. Copy and paste this and fill it according to the instructions within. If in doubt have a look at an existing article.  

The key points are:
* There is a set of metadata at the top of each file. Make sure to fill this out
* Below the metadata, write your report
* Markdown syntax is simple and avialable online. Look it up, or look at another article to format yours. [Also check this](https://help.github.com/articles/markdown-basics/)
* HTML works fine in markdown files (the same as they would in an html file) so if you can't do something with markdown just stick the html in.

##Finishing
Save your .md file. Track the file in git:

    git add path/to/file

Commit your file(s):

    git commit -m "Put descriptive message here"

Please put in a good descirption of what you have done. E.g "Added a trip report for Yorkshire 3 15/03/15".  
Finally push your changes:

    git push

And that can be it. Contact whoever is in charge of the site to let them know to update it. If you want to see it yourself (good to check for formatting errors) then run:

    ./develop_server.sh start

This will start a web server and display the site for you locally. Navigate to localhost:8000 with your web browser to see it. It is likely that images won't show up.

    ./develop_server.sh stop

Will stop the sever.

#Advanced Set Up
If you want to be able to build and deploy the site yourself look here, otherwise ignore.
###Installing Pelican
First make sure you have python 3. Python 2 will not work, it doesn't do unicode easily so I can't be bothered with it.

Pelican is a python based static site generator. Install it:

    pip install pelican

Install the Markdown package as that is what the trip reports should be written in:

    pip install Markdown

Install BeautifulSoup:

    pip install beautifulsoup4

Firstly run:

    pelican content -s publishconf.py

This will build the site and output it to the output folder. To push the site to the union server (and therefore make it live) you will need at least sftp access (can be requested via a sysadmin form). You need to get the contents of the output folder into the /home/www/htdocs/rcc/caving/ folder. If you have ssh access (requested by emailing the sysadmin) then you can run:

    rsync -avz output/ username@dougal.union.ic.ac.uk:/home/www/htdocs/rcc/caving/topsecret

##Photos
The photos are a bit more complicated due to the photo_archive being outside of the root of the nz subsite. To do this you will need at least SFTP access.
* Make folder in appropriate location in photo_archive. e.g "/home/www/htdocs/rcc/caving/photo_archive/newzealand/YYYY-MM-DD%20-%20Placename". Note: %20 is just a space character. Your sftp client can probably handle spaces.
* Upload photos to this folder.
* Run the thumb.sh script that is in photo_archive root from the directory with your new photos. This will generate the thumbnails and small images.
* In the nz subsite there is a photo_archive folder (do not put photos here). From here copy the "index.php" file to your new photo folder.
* In the relevant article, fill out the relevent metadata. (This can be done before making the folder/uploading photos, the links will just be dead until you do)
Done.

#Subsite
There is a plugin that allows subs sites to be added easily (like the NZ or Slov sites). They are treated essentially entirely seperate from the main site so you can have different plugins and completely different themes. Though its probably best just to modfiy the colour scheme slightly :P.
###Set up
It works like the main site. There is a content folder to put articles in, a plug in folder for site specific plugins, a themes folder for a site specific theme. The settings file is a little different. It has to be called "settings.py" and reside in the root of the subsite.

In "settings.py" there are two mandatory settings:

    PATH = 'content'

This should point to the folder that your markdown files are in.

    SUBSITE_PATH = 'newzealand'

This should be the name of the subdirectory you want the site to reside in once its published.

All other settings are optional and will default to the main site's settings. All of the file paths in this settings file will be relative to the file itself (i.e not the main site root). Useful settings to change might be the THEME, PLUGINS, PLUGIN_PATHS or STATIC_PATHS which will copy directories in the subsites content folder into the subsites output (just like for the main site).
