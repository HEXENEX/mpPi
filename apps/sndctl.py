# apps/sndctl/__init__.py

from PIL import ImageDraw, Image, ImageFont, Image
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from io import BytesIO
import select
import time
import vlc
import sys

# persistent player instance
song_path = "library/Music/sauceintherough (bonus track) - brakence.mp3"
volume = 40
player = None
device = None
serial = None
font = None

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


def init_once():
    global player, serial, device, font

    if player is not None:
        return  # already initialized

    instance = vlc.Instance('--aout', 'alsa')
    player = instance.media_player_new()
    media = instance.media_new(song_path)
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()

    serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
    device = st7789(serial, width=320, height=240, rotate=0)
    font = ImageFont.truetype("assets/NotoSansMono_Condensed-SemiBold.ttf", 20)

def update_screen():
    global player, device, font
    img = Image.new("RGB", device.size, "white")
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, 320, 24), fill=(225, 225, 225))
    draw.text((110, 0), "Now Playing", font=font, fill="black")

    current_index = 1
    total_songs = 1
    draw.text((6, 30), f"{current_index} of {total_songs}", font=font, fill="black")

    shuffle = True
    if shuffle:
        draw.text((6, 190), "🔀", font=font, fill="black")

    try:
        total_ms = player.get_length()
        elapsed_ms = player.get_time()

        if total_ms > 0 and elapsed_ms >= 0:
            total_sec = total_ms // 1000
            elapsed_sec = elapsed_ms // 1000
            remaining_sec = total_sec - elapsed_sec

            def format_time(sec):
                return f"{sec // 60}:{sec % 60:02}"

            draw.text((10, 205), format_time(elapsed_sec), font=font, fill="black")
            draw.text((260, 205), f"-{format_time(remaining_sec)}", font=font, fill="black")

            bar_width = 260
            bar_height = 15
            bar_x = 30
            bar_y = 185
            progress = int((elapsed_sec / total_sec) * bar_width)
            draw.rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + bar_height), fill=(225, 225, 225))
            draw.rectangle((bar_x, bar_y, bar_x + progress, bar_y + bar_height), fill=(44, 121, 199))

    except:
        pass

    # metadata
    try:
        audio = MP3(song_path, ID3=ID3)
        tags = audio.tags
        title = tags.get("TIT2", "Unknown Title").text[0]
        artist = tags.get("TPE1", "Unknown Artist").text[0]
        album = tags.get("TALB", "Unknown Album").text[0]

        y = 68
        draw.text((130, y), title, font=font, fill="black")
        draw.text((130, y + 33), album, font=font, fill="black")
        draw.text((130, y + 66), artist, font=font, fill="black")

        for tag in tags.values():
            if isinstance(tag, APIC):
                album_art = Image.open(BytesIO(tag.data)).convert("RGB")
                album_art = album_art.resize((100, 100))
                img.paste(album_art, (15, 65))
                break

    except:
        draw.text((10, 60), "Metadata error", font=font, fill="red")

    device.display(img)

def launch_ui():
    global show_player
    show_player = True
    init_once()

    while show_player:
        input_handler()
        update_screen()
        time.sleep(1 / 16)
