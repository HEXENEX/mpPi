from luma.core.interface.serial import spi
from luma.lcd.device import st7789
from PIL import ImageDraw, Image, ImageFont
import time
import RPi.GPIO as GPIO

buspeed = 52 * 1000000

serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=27, bus_speed_hz=buspeed)
device = st7789(serial, width=320, height=240, rotate=0)


# draw test text
img = Image.new("RGB", device.size, "black")
font = ImageFont.truetype("Sans.ttf", 28)
draw = ImageDraw.Draw(img)
draw.rectangle((0, 0, 319, 239), fill="white")
draw.text((0, 0), "Hello DietPi", font=font, fill="black")



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)
pwm.start(100) # 100 on

device.display(img)

time.sleep(2)

pwm.ChangeDutyCycle(50)
time.sleep(2)

pwm.ChangeDutyCycle(25)
time.sleep(2)

pwm.ChangeDutyCycle(1)
time.sleep(2)