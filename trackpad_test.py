import spidev
import RPi.GPIO as GPIO
import time

DR_PIN = 22
CS_PIN = 7   # GPIO7 connected to SS on the pad

GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN)
GPIO.setup(CS_PIN, GPIO.OUT, initial=GPIO.HIGH)  # CS idle high

spi = spidev.SpiDev()
spi.open(0, 0)      # bus 0, device 0 (we manage CS manually)
spi.no_cs = True
spi.max_speed_hz = 1000000
spi.mode = 0b01      # CPOL=0, CPHA=1

def cs_low():
    GPIO.output(CS_PIN, GPIO.LOW)
    time.sleep(0.00002)  # tiny settle

def cs_high():
    GPIO.output(CS_PIN, GPIO.HIGH)
    time.sleep(0.00002)

def write_register(addr, value):
    """Send a register write: addr + value"""
    cs_low()
    spi.xfer2([addr & 0x7F, value])  # MSB=0 for write
    cs_high()

def read_register(addr):
    """Read a register: send addr + dummy, read response"""
    cs_low()
    resp = spi.xfer2([addr | 0x80, 0x00])  # MSB=1 for read
    cs_high()
    return resp[1]

# --- Initialization sequence ---
# 1. Put device into absolute reporting mode
# 2. Enable data-ready interrupts
# 3. Clear status registers

# These register addresses/values are from Cirque sample demo
# Adjust values if your pad needs relative mode
ABS_MODE_REG = 0x41
DR_ENABLE_REG = 0x40
STATUS_REG   = 0x00

write_register(ABS_MODE_REG, 0x01)     # absolute mode on
write_register(DR_ENABLE_REG, 0x01)    # enable DR pulses
write_register(STATUS_REG, 0x00)       # clear status

time.sleep(0.01)  # 10 ms settle

# --- Test reading packets ---
def read_packet():
    """Read 5-byte touch packet"""
    cs_low()
    pkt = spi.xfer2([0x00]*5)
    cs_high()
    return pkt

print("Touch the pad and watch output. Press Ctrl+C to stop.")
try:
    while True:
        if GPIO.input(DR_PIN):
            pkt = read_packet()
            status = pkt[0]
            x = pkt[1] | (pkt[2] << 8)
            y = pkt[3] | (pkt[4] << 8)
            print(f"Status={status:02X}, X={x}, Y={y}")
        time.sleep(0.002)
except KeyboardInterrupt:
    pass
finally:
    spi.close()
    GPIO.cleanup()
