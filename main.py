from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO

serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=40000000)
device = st7789(serial, width=320, height=240, rotate=0)


# draw splash screen
img = Image.new("RGB", device.size, "black")
font = ImageFont.truetype("assets/Sans.ttf", 28)
draw = ImageDraw.Draw(img)
draw.rectangle((0, 0, 319, 239), fill="white")
draw.text((1, 1), "Welcome DietPi", font=font, fill="black")
draw.text((1, 30), "Play Shit", font=font, fill="black")



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(100) # 100 on

device.display(img)


# loop
time.sleep(5)
pwm.ChangeDutyCycle(1)
time.sleep(5)