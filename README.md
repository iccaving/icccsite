# nzsite

to publish to site run:
$ pelican content -s publishconf.py
$ rsync -avz --delete output/ username@dougal.union.ic.ac.uk:/home/www/htdocs/rcc/caving/newzealand
