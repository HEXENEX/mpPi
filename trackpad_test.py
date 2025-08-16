import spidev
import RPi.GPIO as GPIO
import time

# Pin definitions
DR_PIN = 22   # Data Ready
CE_PIN = 7    # Chip Select for trackpad
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.HIGH)  # CE inactive

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)           # SPI bus 0, device 0 (CE manually controlled)
spi.max_speed_hz = 500000
spi.mode = 0b01           # SPI_MODE1, matches Arduino example

# RAP masks
WRITE_MASK = 0x80
READ_MASK  = 0xA0

# Register config values (from Arduino example)
SYSCONFIG_1   = 0x00
FEEDCONFIG_1  = 0x03
FEEDCONFIG_2  = 0x1F
Z_IDLE_COUNT  = 0x05

# Helper functions
def ce_low(): GPIO.output(CE_PIN, GPIO.LOW)
def ce_high(): GPIO.output(CE_PIN, GPIO.HIGH)

def rap_write(address, value):
    cmd = WRITE_MASK | address
    ce_low()
    spi.xfer2([cmd, value])
    ce_high()
    time.sleep(0.001)

def rap_read(address, count=1):
    cmd = READ_MASK | address
    ce_low()
    result = spi.xfer2([cmd] + [0xFC]*count)
    ce_high()
    return result[1:]  # skip first dummy byte

# Clear status flags
def clear_flags():
    rap_write(0x02, 0x00)
    time.sleep(0.001)

# Enable feed (bit 0 of 0x04)
def enable_feed(enable=True):
    val = rap_read(0x04, 1)[0]
    if enable:
        val |= 0x01
    else:
        val &= ~0x01
    rap_write(0x04, val)
    time.sleep(0.001)

# Initialization sequence
def trackpad_init():
    clear_flags()
    rap_write(0x03, SYSCONFIG_1)
    rap_write(0x05, FEEDCONFIG_2)
    rap_write(0x04, FEEDCONFIG_1)
    rap_write(0x0A, Z_IDLE_COUNT)
    enable_feed(True)
    time.sleep(0.01)

# Read absolute coordinates
def read_touch():
    clear_flags()  # prevent DR from freezing
    # Check DR first
    if GPIO.input(DR_PIN) == 0:
        data = rap_read(0x12, 6)
        buttonFlags = data[0] & 0x3F
        x = data[2] | ((data[4] & 0x0F) << 8)
        y = data[3] | ((data[4] & 0xF0) << 4)
        z = data[5] & 0x3F
        touchDown = x != 0
        return x, y, z, buttonFlags, touchDown
    else:
        return None

# Main
trackpad_init()
print("Trackpad initialized. Touch the pad...")

try:
    while True:
        result = read_touch()
        if result:
            x, y, z, flags, down = result
            if down:
                print(f"X={x}, Y={y}, Z={z}, Buttons={flags}, TouchDown={down}")
            else:
                print("No touch detected")
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    spi.close()
    GPIO.cleanup()
