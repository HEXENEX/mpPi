#
#   Welcome to SoundControl (sndctl)
#

from PIL import ImageDraw, Image, ImageFont
from luma.core.interface.serial import spi
import xml.etree.ElementTree as ET
from luma.lcd.device import st7789
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import RPi.GPIO as GPIO
import time
import vlc

# global vars
is_running = True
volume = 40
song_path = "library/Music/sauceintherough (bonus track) - brakence.mp3"
player = None

# appearance settings
backlight_brightness = 100
font_size = 20
label_margin = 4

# colors
bg_color = "white"
header_color = (225, 225, 225)
text_color = "black"
highlight_color = (44, 121, 199)
hl_text_color = "white"

# init screen + backlight
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
device = st7789(serial, width=320, height=240, rotate=0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(backlight_brightness)

def input_handler():
    global select_idx, current_menu_options

    sim_mode = True
    if sim_mode:
        print("sim input mode")
        u_input = input("input: ")

        update_screen()


def init_player():
    global player

    instance = vlc.Instance('--aout', 'alsa')  # force ALSA only
    player = instance.media_player_new()
    media = instance.media_new(song_path)
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()


def update_screen():
    # background
    img = Image.new("RGB", device.size, bg_color)
    font = ImageFont.truetype("assets/NotoSansMono_Condensed-SemiBold.ttf", font_size)
    draw = ImageDraw.Draw(img)

    # header
    header_margin = font_size + label_margin
    draw.rectangle((0, 0, 320, header_margin), fill=header_color)
    draw.text((110, label_margin - 6), "Now Playing", font=font, fill=text_color)


    # playerUI
    # playlist
    current_index = 1
    total_songs = 28
    draw.text((6, 28), f"{current_index} of {total_songs}", font=font, fill=text_color)

    # draw playback bar with time elasps on the left, and time left on the right
    # playback bar
    if player is not None:
        try:
            total_ms = player.get_length()
            elapsed_ms = player.get_time()

            if total_ms > 0 and elapsed_ms >= 0:
                total_sec = total_ms // 1000
                elapsed_sec = elapsed_ms // 1000
                remaining_sec = total_sec - elapsed_sec

                def format_time(sec):
                    return f"{sec // 60}:{sec % 60:02}"

                

                # progress bar
                bar_width = 260
                bar_height = 15
                bar_x = 30
                bar_y = 185

                # time text
                draw.text((10, 205), format_time(elapsed_sec), font=font, fill=text_color)
                draw.text((260, 205), f"-{format_time(remaining_sec)}", font=font, fill=text_color)

                progress = int((elapsed_sec / total_sec) * bar_width)

                draw.rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + bar_height), fill=header_color)
                draw.rectangle((bar_x, bar_y, bar_x + progress, bar_y + bar_height), fill=highlight_color)

        except:
            pass

    # get mp3 metadata
    try:
        audio = MP3(song_path, ID3=ID3)
        tags = audio.tags

        title = tags.get("TIT2", "Unknown Title").text[0]
        artist = tags.get("TPE1", "Unknown Artist").text[0]
        album = tags.get("TALB", "Unknown Album").text[0]

        # Display metadata
        y = 64
        draw.text((130, y), title, font=font, fill=text_color)
        draw.text((130, y + 33), album, font=font, fill=text_color)
        draw.text((130, y + 2*33), artist, font=font, fill=text_color)

        # Display album art
        for tag in tags.values():
            if isinstance(tag, APIC):
                from io import BytesIO
                album_art = Image.open(BytesIO(tag.data)).convert("RGB")
                album_art = album_art.resize((100, 100))
                img.paste(album_art, (15, 65))  # Adjust as needed
                break

    except Exception as e:
        draw.text((label_margin, 60), f"Metadata error", font=font, fill="red")

    # draw screen
    device.display(img)

# --- Runtime --- #

try:
    # --- startup commands --- #
    update_screen()
    init_player()

    while is_running:
        #input_handler()
        update_screen()

        #time.sleep(0.5)
        time.sleep(0.0625)
        #time.sleep(0.0167)

except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()