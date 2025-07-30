from PIL import ImageDraw, Image, ImageFont
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
import xml.etree.ElementTree as ET
import RPi.GPIO as GPIO
import select
import time
import sys

# importing apps
import apps.sndctl as sndctl
import apps.mklib as mklib


# global vars
is_running = True
menu_idx = 0
current_menu = []
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

# backlight pwm
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

            update_screen(current_menu, menu_idx)

def menu_up():
    global menu_idx
    if menu_idx > 0:
        menu_idx -= 1

def menu_down():
    global menu_idx
    if menu_idx < len(current_menu) - 1:
        menu_idx += 1

def select_press():
    global menu_idx, current_menu
    selected_item = current_menu[menu_idx]
    submenu = selected_item.find("submenu")
    app = selected_item.attrib.get("app")

    if submenu is not None:
        # Save current screen's menu and index
        menu_stack.append((current_menu, menu_idx))
        menu_idx = 0
        current_menu = list(submenu.findall("item"))

    if app is not None:
        if app == "sndctl":
            sndctl.launch_ui()

def menu_press():
    global menu_idx, current_menu
    if menu_stack:
        prev_menu_options, prev_idx = menu_stack.pop()
        current_menu = prev_menu_options
        menu_idx = prev_idx
    else:
        current_menu = load_menu_root()
        menu_idx = 0

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
    current_menu = load_menu_root()
    update_screen(current_menu, menu_idx)

    while is_running:
        input_handler()
        time.sleep(1 / 16)

except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()
