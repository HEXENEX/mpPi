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
                    print("is mp3")
                    # full path of file
                    full_path = os.path.join(dirpath, file)
                    song_id += 1
                    
                    audio = MP3(full_path, ID3=ID3)
                    tags = audio.tags

                    print("getting tags")
                    # find mp3 metadata
                    title = tags.get("TIT2", "Unknown Title").text[0]
                    album = tags.get("TALB", "Unknown Album").text[0]
                    artist = tags.get("TPE1", "Unknown Artist").text[0]
                    album_artist = tags.get("TPE2", "Unknown Artist").text[0]
                    genre = tags.get("TCON", "Unknown Genre").text[0]
                    track_num = tags.get("TRCK", "Unknown Track Number").text[0]
                    disc_num = tags.get("TPOS", "Unknown Disc Number").text[0]
                    year = tags.get("TDRC", "Unknown Year").text[0] or tags.get("TYER", "Unknown Year").text[0]
                    comment = tags.get("COMM::'eng'", "Unknown Comment").text[0]
                    rating = tags.get("POPM", "Unknown Rating").text[0]
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