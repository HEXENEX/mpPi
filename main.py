from PIL import ImageDraw, Image, ImageFont
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import subprocess
import select
import time
import sys

# importing apps
import apps.sndctl as sndctl


# global vars
is_running = True
select_idx = 0
current_menu_options = []
menu_stack = []

# appearance settings
backlight_brightness = 100
font_size = 22
label_margin = 4

# colors
bg_color = "white"
header_color = (180, 180, 180)
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

            update_screen(current_menu_options, select_idx)

def menu_up():
    global select_idx
    if select_idx > 0:
        select_idx -= 1

def menu_down():
    global select_idx
    if select_idx < len(current_menu_options) - 1:
        select_idx += 1

def select_press():
    global select_idx, current_menu_options
    selected_item = current_menu_options[select_idx]
    submenu = selected_item.find("submenu")
    app = selected_item.attrib.get("app")

    if submenu is not None:
        menu_stack.append(submenu)
        select_idx = 0
        current_menu_options = list(submenu.findall("item"))

    if app is not None:
        if app == "sndctl":
            sndctl.launch_ui()

def menu_press():
    global select_idx, current_menu_options
    if menu_stack:
        menu_stack.pop()
        if menu_stack:
            current_menu_options = list(menu_stack[-1].findall("item"))
        else:
            current_menu_options = load_menu_root()
        select_idx = 0

def skip_press():
    pass

def pauseplay_press():
    pass

def prev_press():
    pass

def load_menu_root(menu_file="menu.xml"):
    tree = ET.parse(menu_file)
    root = tree.getroot()
    menu_stack.clear()
    return list(root.findall("item"))

def update_screen(menu_options, selected_index):
    text_offset = -4
    img = Image.new("RGB", device.size, bg_color)
    font = ImageFont.truetype("assets/NotoSansMono_Condensed-SemiBold.ttf", font_size)
    draw = ImageDraw.Draw(img)

    header_margin = font_size + label_margin
    draw.rectangle((0, 0, 320, header_margin), fill=header_color)
    draw.text((130, label_margin - 6), "Menu", font=font, fill=text_color)

    for i, item in enumerate(menu_options):
        label = item.attrib.get("label", "")
        y = i * (font_size + label_margin)

        if i == selected_index:
            draw.rectangle((0, y + header_margin, 320, y + font_size + label_margin + header_margin), fill=highlight_color)
            draw.text((label_margin, y + header_margin + text_offset), label, font=font, fill=hl_text_color)
        else:
            draw.text((label_margin, y + header_margin + text_offset), label, font=font, fill=text_color)

    device.display(img)

# --- Runtime --- #

try:
    current_menu_options = load_menu_root()
    update_screen(current_menu_options, select_idx)

    while is_running:
        input_handler()
        time.sleep(1 / 16)

except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()
