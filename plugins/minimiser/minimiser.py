from pelican import signals, utils
import os
import sass
import logging


def minimise(pel):
    for root, dirs, files in os.walk(os.path.join(pel.settings["OUTPUT_PATH"], pel.settings["THEME_STATIC_DIR"])):
        for afile in files:
            filename, file_extension = os.path.splitext(afile)
            if file_extension == ".scss" and filename[0] != "_":
                f = open(os.path.join(root, filename + ".css"), "w")
                f.write(sass.compile(filename=os.path.join(root, afile), output_style='compressed'))
                f.close()

    for root, dirs, files in os.walk(os.path.join(pel.settings["OUTPUT_PATH"], pel.settings["THEME_STATIC_DIR"])):
        for afile in files:
            filename, file_extension = os.path.splitext(afile)
            if file_extension == ".scss":
                os.remove(os.path.join(root, afile))

    for root, dirs, files in os.walk(os.path.join(pel.settings["OUTPUT_PATH"], pel.settings["THEME_STATIC_DIR"])):
        for adir in dirs:
            try:
                os.rmdir(os.path.join(root, adir))
            except OSError as ex:
                pass


def register():
    signals.finalized.connect(minimise)
