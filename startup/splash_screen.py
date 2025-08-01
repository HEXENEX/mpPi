from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO

serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=36000000)
device = st7789(serial, width=320, height=240, rotate=0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(100) # backlight 100% on

# draw
img = Image.new("RGB", device.size, "black")
draw = ImageDraw.Draw(img)

# draw splash logo
art = Image.open("assets/mpPilogo.png").convert("RGBA").resize((240, 240))
img.paste(art, (40, -10))

device.display(img)
time.sleep(5)
GPIO.output(18, GPIO.LOW) # turns off backlight
GPIO.cleanup()