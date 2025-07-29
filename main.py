import xml.etree.ElementTree as ET
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO


# global vars
is_running = True

# init var
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
device = st7789(serial, width=320, height=240, rotate=0)


def load_menu(menu_tree="menu.xml"):
    root = ET.fromstring(menu_tree)

    for element, label in root:
        print(element)
        print(f"    {label}")

    print("loaded menu")
    return

def draw_screen():
    # Background color
    img = Image.new("RGB", device.size, "white")
    font = ImageFont.truetype("assets/Sans.ttf", 28)
    draw = ImageDraw.Draw(img)

    # menu text
    draw.text((1, 1), "Resume Playing", font=font, fill="black")
    draw.text((1, 30), "Songs", font=font, fill="black")
    draw.text((1, 60), "Playlists", font=font, fill="black")
    draw.text((1, 90), "Settings", font=font, fill="black")
    draw.text((1, 120), "About", font=font, fill="black")

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    pwm = GPIO.PWM(18, 1000)
    pwm.start(100) # 100 on

    device.display(img)

    return

# runtime loop
while is_running == True:
    load_menu()
    time.sleep(0.0625) # pause for 1/16 of a second, making it 16fps