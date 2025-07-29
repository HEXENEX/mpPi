from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO

serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
device = st7789(serial, width=320, height=240, rotate=0)


# draw test text
img = Image.new("RGB", device.size, "black")
draw = ImageDraw.Draw(img)
draw.rectangle((0, 0, 320, 240), fill="black")
draw.text((160, 120), "Pulling Repository", fill="white")


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(100) # 100 on

device.display(img)
time.sleep(1)