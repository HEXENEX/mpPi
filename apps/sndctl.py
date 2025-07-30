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


# appearance settings
backlight_brightness = 100
font_size = 22
label_margin = 4

# colors
bg_color = "white"
header_color = "grey"
text_color = "black"
highlight_color = (44, 121, 199)
hl_text_color = "white"

# init screen + backlight
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=52000000)
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
    instance = vlc.Instance('--aout', 'alsa')  # force ALSA only
    player = instance.media_player_new()
    media = instance.media_new("library/Music/Death Roll - Wage War.mp3")
    player.set_media(media)
    player.audio_set_volume(volume)
    player.play()

def update_screen():
    # background
    img = Image.new("RGB", device.size, bg_color)
    font = ImageFont.truetype("assets/Sans.ttf", font_size)
    draw = ImageDraw.Draw(img)

    # header (+plus clock?)
    draw.rectangle((0, 0, 320, font_size + label_margin), fill=header_color)

    # playerUI
    draw.text((label_margin, 120 + (label_margin / 2)), "player", font=font, fill=text_color)

    device.display(img)

# --- Runtime --- #

try:
    # --- startup commands --- #
    update_screen()
    init_player()

    while is_running:
        #input_handler()
        time.sleep(0.0625)

except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()
