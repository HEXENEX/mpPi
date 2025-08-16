import RPi.GPIO as GPIO
import time

DR_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN)

print("Watching DR pin on GPIO22. Touch the pad... (Ctrl+C to exit)")
try:
    while True:
        val = GPIO.input(DR_PIN)
        print("DR =", val)
        time.sleep(0.05)  # 20 Hz refresh
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
