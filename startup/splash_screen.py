import spidev
import RPi.GPIO as GPIO
import time

DR_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN)

spi = spidev.SpiDev()
spi.open(0, 1)          # bus 0, CE1 (GPIO7)
spi.max_speed_hz = 1000000
spi.mode = 0b01

try:
    print("Move your finger... Press Ctrl+C to exit")
    while True:
        if GPIO.input(DR_PIN):
            data = spi.readbytes(5)
            print("Packet:", [f"{b:02X}" for b in data])
        time.sleep(0.001)
except KeyboardInterrupt:
    pass
finally:
    spi.close()
    GPIO.cleanup()
