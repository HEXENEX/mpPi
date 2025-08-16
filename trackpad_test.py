import spidev
import RPi.GPIO as GPIO
import time

# --- GPIO setup ---
DR_PIN = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN)

# --- SPI setup ---
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus 0, CE0)
spi.max_speed_hz = 1000000  # 1 MHz is safe to start
spi.mode = 0b01             # Mode 1 is typical for Cirque Pinnacle
spi.bits_per_word = 8

# --- Helper functions ---
def spi_write_then_read(write_data, read_len):
    """Write bytes, then read back."""
    spi.xfer2(write_data)
    return spi.readbytes(read_len)

def read_register(reg_addr, length=1):
    """Read register from TM040040."""
    # Datasheet defines command format (example: MSB=1 for read)
    cmd = [reg_addr | 0x80]  # set read flag
    return spi_write_then_read(cmd, length)

def write_register(reg_addr, value):
    """Write register to TM040040."""
    # MSB=0 for write
    spi.xfer2([reg_addr & 0x7F, value])

# --- Main loop ---
print("Waiting for trackpad input (Ctrl+C to exit)...")

try:
    while True:
        if GPIO.input(DR_PIN) == GPIO.HIGH:
            # Example: read motion packet (assuming starts at 0x12)
            packet = read_register(0x12, 5)  # length depends on mode
            print("Packet:", packet)
        time.sleep(0.001)  # 1 ms poll
except KeyboardInterrupt:
    pass
finally:
    spi.close()
    GPIO.cleanup()
