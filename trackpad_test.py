import spidev
import RPi.GPIO as GPIO
import time

# --- GPIO Setup ---
DR_PIN = 22  # Connect Data Ready (DR) pin here
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- SPI Setup ---
spi = spidev.SpiDev()
spi.open(0, 0)           # bus 0, device 0 (CE0)
spi.max_speed_hz = 1000000  # 1 MHz
spi.mode = 0b01           # CPOL=0, CPHA=1 (typical for TM040040)
spi.bits_per_word = 8

# --- Read Touch Data ---
def read_touch():
    """
    Reads 4 bytes from TM040040 (example: X1, Y1, X2, Y2 for 2 fingers)
    """
    # Wait for DR pin to go low (data ready)
    while GPIO.input(DR_PIN) == 1:
        time.sleep(0.001)

    # Typical sequence: write 0x00 to request touch report
    spi.xfer2([0x00])
    time.sleep(0.001)

    # Read 4 bytes: X1, Y1, X2, Y2
    data = spi.readbytes(4)
    return data

# --- Main Loop ---
try:
    while True:
        touch_data = read_touch()
        x1, y1, x2, y2 = touch_data
        print(f"Finger 1: ({x1},{y1}), Finger 2: ({x2},{y2})")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    spi.close()
    GPIO.cleanup()
