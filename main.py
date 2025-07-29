import xml.etree.ElementTree as ET
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO

# global vars
is_running = True
select_idx = 0
current_menu_options = []

# appearance settings
backlight_brightness = 100
font_size = 22
label_margin = 4
text_color = "black"
hl_text_color = "white"
bg_color = "white"
highlight_color = (44, 121, 199)

# init screen + backlight
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=52000000)
device = st7789(serial, width=320, height=240, rotate=0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(backlight_brightness)

# --- Menu Logic --- #

def input_handler():
    global select_idx
    sim_mode = True

    if sim_mode:
        print("sim input mode")
        u_input = input("input: ")

        if u_input == "w":  # down
            if select_idx < len(current_menu_options) - 1:
                select_idx += 1
        elif u_input == "x":  # up
            if select_idx > 0:
                select_idx -= 1

        update_screen(current_menu_options, select_idx)


def load_menu(menu_file="menu.xml"):
    menu_options = []
    root = ET.parse(menu_file).getroot()

    for item in root.findall("item"):
        label = item.attrib.get("label", "")
        if label:
            menu_options.append(label)

    return menu_options


def update_screen(menu_options, selected_index):
    img = Image.new("RGB", device.size, bg_color)
    font = ImageFont.truetype("assets/Sans.ttf", font_size)
    draw = ImageDraw.Draw(img)

    for i, label in enumerate(menu_options):
        y = i * (font_size + label_margin)
        if i == selected_index:
            draw.rectangle((0, y, 320, y + font_size + label_margin), fill=highlight_color)
            draw.text((label_margin, y), label, font=font, fill=hl_text_color)
        else:
            draw.text((label_margin, y), label, font=font, fill=text_color)

    device.display(img)

# --- Runtime --- #

try:
    current_menu_options = load_menu()
    update_screen(current_menu_options, select_idx)

    while is_running:
        input_handler()
        time.sleep(0.0625)

except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()
