import xml.etree.ElementTree as ET
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO


# global vars
is_running = True
backlight_brightness = 100
font_size = 28
label_margin = 2
text_color = "black"
bg_color = "white"
highlight_color = "blue"

# init var
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
device = st7789(serial, width=320, height=240, rotate=0)


def load_menu(menu_file="menu.xml"):
    root = ET.parse(menu_file)
    menu_options = []

    for item in root.findall("item"):
        menu_options.append(item.attrib.get("label"))

    print(menu_options)
    return

def draw_screen(menu_options=[]):
    # Background color
    img = Image.new("RGB", device.size, bg_color)
    font = ImageFont.truetype("assets/Sans.ttf", font_size)
    draw = ImageDraw.Draw(img)

    # add menu text options
    x_offset = label_margin
    y_offset = label_margin
    for label in menu_options:
        draw.text((x_offset, y_offset), label, font=font, fill=text_color)
        y_offset += font_size + label_margin


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 1000)
    pwm.start(backlight_brightness) # 100 on

    device.display(img)

    return


# runtime loop
menu = load_menu()  # only load once at start
draw_screen()       # draw once

try:
    while is_running:
        # put update logic here if needed
        time.sleep(0.0625)  # ~16 fps if needed
except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()