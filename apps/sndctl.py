# apps/sndctl/__init__.py

from PIL import ImageDraw, Image, ImageFont, ImageOps, Image
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from io import BytesIO
import select
import time
import vlc
import sys

# --- Constants ---
volume = 40

# --- Globals ---
player = None
device = None
font = None
metadata_cache = None
album_art_cache = None
show_player = True

def input_handler():
    sim_mode = True
    if sim_mode:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            u_input = sys.stdin.readline().strip()

            if u_input == "r":
                menu_up()
            elif u_input == "f":
                menu_down()
            elif u_input == "s":
                select_press()
            elif u_input == "w":
                menu_press()
            elif u_input == "d":
                skip_press()
            elif u_input == "x":
                pauseplay_press()
            elif u_input == "a":
                prev_press()

def menu_up():
    print("Volume down")

def menu_down():
    print("Volume down")

def select_press():
    print("show next menu")

def menu_press():
    global show_player
    print("go back to main menu (with audio still playing)")
    show_player = False

def skip_press():
    print("skip to next song")

def pauseplay_press():
    print("pause current song")

def prev_press():
    print("replay song / go to prev song if in first 1 second of play")


# --- Initialization ---
def init_once(song_path):
    global player, serial, device, font, shuffle_icon

    if player:
        return

    # Set up VLC to use ALSA with Bluetooth (BlueALSA)
    instance = vlc.Instance(
        '--aout=alsa',
        '--alsa-audio-device=bluealsa'  # Or add ":DEV=XX:XX:XX...,PROFILE=a2dp" if needed
    )
    player = instance.media_player_new()
    media = instance.media_new(song_path)
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()

    # Set up LCD
    serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
    device = st7789(serial, width=320, height=240, rotate=0)
    font = ImageFont.truetype("assets/NotoSansMono_Condensed-SemiBold.ttf", 20)



# --- Metadata Caching ---
def load_metadata():
    global metadata_cache, album_art_cache

    if metadata_cache: return metadata_cache, album_art_cache

    try:
        audio = MP3(song_path, ID3=ID3)
        tags = audio.tags
        title = tags.get("TIT2", "Unknown Title").text[0]
        artist = tags.get("TPE1", "Unknown Artist").text[0]
        album = tags.get("TALB", "Unknown Album").text[0]
        metadata_cache = (title, album, artist)

        for tag in tags.values():
            if isinstance(tag, APIC):
                art = Image.open(BytesIO(tag.data)).convert("RGB").resize((100, 100))
                album_art_cache = art
                break
        else:
            album_art_cache = None

    except:
        metadata_cache = ("Unknown", "Unknown", "Unknown")
        album_art_cache = None

    return metadata_cache, album_art_cache


# --- Screen Update ---
def update_screen():
    global player, device, font

    img = Image.new("RGB", device.size, "white")
    draw = ImageDraw.Draw(img)

    # Header
    draw.rectangle((0, 0, 320, 24), fill=(225, 225, 225))
    draw.text((110, -4), "Now Playing", font=font, fill="black")

    # Playlist
    draw.text((8, 30), "1 of 1", font=font, fill="black")

    # Progress bar
    try:
        total_ms = player.get_length()
        elapsed_ms = player.get_time()

        if total_ms > 0 and elapsed_ms >= 0:
            total_sec = total_ms // 1000
            elapsed_sec = elapsed_ms // 1000
            remaining_sec = total_sec - elapsed_sec

            def fmt(sec): return f"{sec // 60}:{sec % 60:02}"

            draw.text((10, 205), fmt(elapsed_sec), font=font, fill="black")
            draw.text((260, 205), f"-{fmt(remaining_sec)}", font=font, fill="black")

            bar_x, bar_y, bar_w, bar_h = 30, 185, 260, 15
            progress = int((elapsed_sec / total_sec) * bar_w)
            draw.rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), fill=(225, 225, 225))
            draw.rectangle((bar_x, bar_y, bar_x + progress, bar_y + bar_h), fill=(44, 121, 199))

    except:
        pass

    # Metadata
    (title, album, artist), art = load_metadata()

    draw.text((130, 68), title, font=font, fill="black")
    draw.text((130, 101), album, font=font, fill="black")
    draw.text((130, 134), artist, font=font, fill="black")

    if art:
        img.paste(art, (15, 65))

    device.display(img)


# --- Main UI Loop ---
def launch_ui(song_path):
    global show_player
    show_player = True
    init_once(song_path)

    while show_player:
        input_handler()
        update_screen()
        time.sleep(1 / 8) 