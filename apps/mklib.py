# apps/mklib/__init__.py

import xml.etree.ElementTree as ET
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TCON, TRCK, TPOS, TYER, COMM, POPM
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
lib_path = "music.lib"

def make_library():
    xml_root = ET.Element("lib")  # don't call this 'root'
    song_id = 0
    try:
        for dirpath, dirs, files in os.walk(music_path):
            print(dirpath)
            for file in files:
                print(file)
                if file.lower().endswith(".mp3"):

                    full_path = os.path.join(dirpath, file)
                    audio = MP3(full_path, ID3=ID3)
                    tags = audio.tags or {}

                    def get_tag(key, default=None):
                        tag = tags.get(key)
                        return tag.text[0] if tag and hasattr(tag, 'text') else default

                    print("get metadata")
                    title = get_tag("TIT2", "Unknown Title")
                    album = get_tag("TALB", "Unknown Album")
                    artist = get_tag("TPE1", "Unknown Artist")
                    album_artist = get_tag("TPE2")
                    genre = get_tag("TCON")
                    track_num = get_tag("TRCK")
                    disc_num = get_tag("TPOS")
                    year = get_tag("TDRC") or get_tag("TYER")
                    comment = get_tag("COMM::'eng'")
                    rating = get_tag("POPM", "Unknown Rating")
                    plays = file.split("_")[0]
                    if plays == file:
                        plays = '0'

                    print("added xml")
                    # add to XML
                    song = ET.SubElement(xml_root, "song")

                    ET.SubElement(song, "song_id").text = str(song_id)
                    ET.SubElement(song, "title").text = title
                    ET.SubElement(song, "album").text = album
                    ET.SubElement(song, "artist").text = artist
                    ET.SubElement(song, "album_artist").text = album_artist
                    ET.SubElement(song, "genre").text = genre
                    ET.SubElement(song, "track_num").text = track_num
                    ET.SubElement(song, "disc_num").text = disc_num
                    ET.SubElement(song, "year").text = year
                    ET.SubElement(song, "comment").text = comment
                    ET.SubElement(song, "rating").text = rating
                    ET.SubElement(song, "plays").text = plays
                    ET.SubElement(song, "path").text = full_path

        print("export xml")
        tree = ET.ElementTree(xml_root)
        ET.indent(tree, space="    ")
        tree.write(lib_path, encoding='utf-8', xml_declaration=True)

        print("Created library.file")
    except:
        print("Failed to make library file")

if __name__ == "__main__":
    make_library()