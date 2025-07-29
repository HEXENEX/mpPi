import xml.etree.ElementTree as ET
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO


# global vars
is_running = True
backlight_brightness = 100
font_size = 26
label_margin = 4
text_color = "black"
hl_text_color = "white"
bg_color = "white"
highlight_color = (44, 121, 199)

# init var
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=52000000)
device = st7789(serial, width=320, height=240, rotate=0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(backlight_brightness) # 100 on


def input_handler():
    # input from GPIO pins and trackpad here
        # but for now it will be simulated
    
    sim_mode = True
    if sim_mode == True:
        print("sim input mode")
        
        u_input = input("input: ")
        
    return


def load_menu(menu_file="menu.xml"):
    root = ET.parse(menu_file)
    menu_options = []

    for item in root.findall("item"):
        menu_options.append(item.attrib.get("label"))

    return menu_options

def update_screen(menu_options=[], idx=0):
    # Background color
    img = Image.new("RGB", device.size, bg_color)
    font = ImageFont.truetype("assets/Sans.ttf", font_size)
    draw = ImageDraw.Draw(img)

    # add highlight box
    draw.rectangle((0, (font_size + label_margin) * idx, 320, (font_size + label_margin) * (idx + 1)), fill=highlight_color)

    # add menu text options
    x_offset = label_margin
    y_offset = label_margin
    for label in menu_options:
        if label == menu_options[idx]:
            # if the menu item is selected text color will be white
            draw.text((x_offset, y_offset), label, font=font, fill=hl_text_color)
        else:
            # if not it will be black
            draw.text((x_offset, y_offset), label, font=font, fill=text_color)
        y_offset += font_size + label_margin

    device.display(img)
    return


# runtime loop
menu_gen = load_menu()  # load once at start
update_screen(menu_gen)   # draw screen

try:
    idx = 0
    while is_running:
        update_screen(menu_gen, idx)
        idx += 1

        if idx > 4:
            idx = 0

        time.sleep(0.5)
        #time.sleep(0.0625)  # refresh rate ~16 fps

except KeyboardInterrupt:
    is_running = False
    GPIO.cleanup()