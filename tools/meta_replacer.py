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
    needs_replacing = False
    pattern = re.escape(pattern)
    match = False
    match_text = "=========Match=========\nPath: " + file_path + "\n"
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                # If a line starts with the metadata section of interest
                # OR there's whitespace and the previous section was of interest
                # (to catch all the Cavepeep lines) then we need to think about
                # replacing things on that line. Otherwise just print the
                # unchanged line in the new file
                if line.startswith(metaitem) or (re.match(r'[ \t]', line) and prevline.startswith(metaitem)):
                    # Always check if there's a match so we have something to
                    # print
                    if re.search(pattern, line) is not None:
                        match = True
                        match_text = match_text + "Line: " + re.sub(pattern, r'\033[4m\033[1m\033[92m\g<0>\033[0m', line.strip()) + "\n"
                    # If we're not just checking (we're actually replacing)
                    if not just_checking:
                        # Do the replacing, write the new line to the new file
                        new_file.write(re.sub(pattern, subst, line))
                        # Need to check if we actually replaced and then print
                        # that we did
                        if re.search(pattern, line) is not None:
                            needs_replacing = True
                            match_text = match_text + "Replaced\n"
                else:
                    new_file.write(line)
                # Make sure we know what the last metadata section was
                if not (re.match(r'[ \t]', line)):
                    prevline = line

    close(fh)
    if match:
        match_text = match_text + "=======================\n"
        print(match_text)
    # If we didn't replace anything in the file we don't replace the file itself
    # this stops git flagging up unchanged but touched files as different
    if needs_replacing:
        remove(file_path)
        move(abs_path, file_path)


def find(begin_date_object, end_date_object, metaitem, metaold, metanew, just_checking):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    replacepath = os.path.abspath(sys.argv[1]).strip()
    # Walk through directoy
    for root, dirs, files in os.walk(replacepath):
        for article in files:
            if os.path.splitext(article)[1] == ".md":
                path = os.path.join(root, article)
                with open(path, 'r') as text:
                    # Get the metadata from the file
                    md.convert(text.read())
                    # Check if file contains metadata section of interest and is
                    # within specified date range
                    possibleypresent = metaitem.lower() in md.Meta.keys()
                    try:
                        notbefore = datetime.strptime(
                            md.Meta['date'][0], '%Y-%m-%d') > begin_date_object
                        notafter = datetime.strptime(
                            md.Meta['date'][0], '%Y-%m-%d') < end_date_object
                    except:
                        notbefore = True
                        notafter = True

                # If the metadata suggests this is a file of interest then delve
                # into it
                if possibleypresent and notbefore and notafter:
                    replace(path, metaitem, metaold, metanew, just_checking)

#==============================================================================
#====================================MAIN======================================
#==============================================================================

if len(sys.argv) < 2:
    print("Error: Wrong number of arguments")
    print("This script takes directory path as its first argument")
    sys.exit()

begin_date_string = "0001-01-01"
end_date_string = "9999-12-31"
metaitem = None
metaold = None
metanew = None

if len(sys.argv) > 2:
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--start":
            begin_date_string = sys.argv[i + 1]
        if sys.argv[i] == "--end":
            end_date_string = sys.argv[i + 1]
        if sys.argv[i] == "--meta":
            metaitem = sys.argv[i + 1]
        if sys.argv[i] == "--pattern":
            metaold = sys.argv[i + 1]
        if sys.argv[i] == "--sub":
            metanew = sys.argv[i + 1]

if metaitem is None or metaold is None or metanew is None:
    print("Enter metadata section [--meta <metadata section>], pattern [--pattern <pattern>] and substitution [--sub <substitution>]")
    sys.exit()

begin_date_object = datetime.strptime(begin_date_string, '%Y-%m-%d')
end_date_object = datetime.strptime(end_date_string, '%Y-%m-%d')

if not begin_date_object < end_date_object:
    print("Enter valid dates <YYYY-MM-DD>, end after start")
    sys.exit()

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
        find(begin_date_object, end_date_object,
             metaitem, metaold, metanew, False)
        sys.exit()
    elif replace_now == 'n':
        sys.exit()
    else:
        print("Type 'y' or 'n'.")
