# apps/mklib/__init__.py

import xml.etree.ElementTree as ET
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import os

# walk through all files in library/Music/
    # if file is a mp3
    # collect tags from file
    # append to xml

# then write to xml file (maybe write as its doing to decrease RAM usage)

import xml.etree.ElementTree as ET
import os

music_path = "library/Music/"
lib_path = "library.xml"

def make_library():
    xml_root = ET.Element("lib")  # don't call this 'root'

    for dirpath, dirs, files in os.walk(music_path):
        for file in files:
            if file.lower().endswith(".mp3"):

                # find mp3 metadata
                title = None
                album = None
                artist = None
                album_artist = None
                genre = None
                track_num = None
                disc_num = None
                year = None
                comment = None
                rating = None

                full_path = os.path.join(dirpath, file)

                # add to XML
                song = ET.SubElement(xml_root, "song")
                ET.SubElement(song, "path").text = full_path

    tree = ET.ElementTree(xml_root)
    ET.indent(tree, space="    ")
    tree.write(lib_path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    make_library()