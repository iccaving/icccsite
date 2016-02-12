from tempfile import mkstemp
from shutil import move
import os
from os import remove, close
import markdown
from datetime import datetime
import re
import sys

def replace(file_path, metaitem, pattern, subst, just_checking):
    # Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line.startswith(metaitem) or (re.match(r'[ \t]', line) and prevline.startswith(metaitem)):
                    if pattern in line:
                        print("Match in: " + file_path)
                    if not just_checking:
                        new_file.write(line.replace(pattern, subst))
                        print("Replaced")
                    elif just_checking:
                        new_file.write(line)
                else:
                    new_file.write(line)
                if not (re.match(r'[ \t]', line)):
                    prevline = line
    close(fh)
    remove(file_path)
    move(abs_path, file_path)

def find(begin_date_object, end_date_object, metaitem, metaold, metanew, just_checking):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    replacepath = os.path.abspath(sys.argv[1]).strip()
    for root, dirs, files in os.walk(replacepath):
        for article in files:
            path = os.path.join(root, article)
            with open(path, 'r') as text:
                md.convert(text.read())
                possibleypresent = metaitem.lower() in md.Meta.keys()
                notbefore = datetime.strptime(
                    md.Meta['date'][0], '%Y-%m-%d') > begin_date_object
                notafter = datetime.strptime(
                    md.Meta['date'][0], '%Y-%m-%d') < end_date_object
            if possibleypresent and notbefore and notafter:
                replace(path, metaitem, metaold, metanew, just_checking)

#==============================================================================
#====================================MAIN======================================
#==============================================================================

if len(sys.argv) != 2:
    print("Error: Wrong number of arguments")
    print("This script takes directory path as its sole argument")
    sys.exit()

print("What date range should be considered?")
valid = False
while not valid:
    begin_date_string = input("Enter the beginnining date <YYYY-MM-DD>: ")
    begin_date_object = datetime.strptime(begin_date_string, '%Y-%m-%d')

    end_date_string = input("Enter the end date <YYYY-MM-DD>: ")
    end_date_object = datetime.strptime(end_date_string, '%Y-%m-%d')

    if begin_date_object < end_date_object:
        valid = True


metaitem = input("Enter the metadata key are you replacing a member of: ")
metaold = input("Enter the value you would replaced: ")
metanew = input("Enter the replacement value: ")

print("You would like '" + metaold + "' replaced with '" +
      metanew + "' in the '" + metaitem + "' section of metadata.")

valid = False
while not valid:
    just_checking_string = input("See list of affected articles? <y/n>: ")
    if just_checking_string == 'y':
        just_checking = True
        valid = True
    elif just_checking == 'n':
        just_checking = False
        valid = True
    else:
        print("Type 'y' or 'n'.")

if just_checking:
    find(begin_date_object, end_date_object, metaitem, metaold, metanew, True)

valid = False
while not valid:
    replace_now = input("Replace now? <y/n>: ")
    if replace_now == 'y':
        find(begin_date_object, end_date_object, metaitem, metaold, metanew, False)
        sys.exit()
    elif replace_now == 'n':
        sys.exit()
    else:
        print("Type 'y' or 'n'.")
