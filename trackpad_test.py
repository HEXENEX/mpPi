import spidev
import RPi.GPIO as GPIO
import time

# GPIO setup
DR_PIN = 22   # Data Ready pin from trackpad
CS_PIN = 7    # Chip Select (SS)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 1)  # Bus 0, Device 1 (CE1 = GPIO7)
spi.max_speed_hz = 1000000  # 1 MHz, trackpad spec allows up to ~2MHz
spi.mode = 0b01             # CPOL=0, CPHA=1 (Cirque datasheet requirement)

def read_packet():
    """
    Read a 5-byte data packet from the TM040040.
    Packet format (from Cirque docs):
    [status, x_lo, x_hi, y_lo, y_hi]
    """
    # Assert CS manually (if needed, spidev can handle it but we’ll be explicit)
    data = spi.readbytes(5)
    return data

try:
    print("Starting trackpad test. Move your finger... Press Ctrl+C to stop.")
    while True:
        # Wait for DR to signal data available
        if GPIO.input(DR_PIN) == 1:
            packet = read_packet()
            if len(packet) == 5:
                status = packet[0]
                x = packet[1] | (packet[2] << 8)
                y = packet[3] | (packet[4] << 8)
                print(f"Status={status:02X}, X={x}, Y={y}")
        time.sleep(0.001)  # tiny delay to avoid busy-looping
except KeyboardInterrupt:
    print("Exiting.")
finally:
    spi.close()
    GPIO.cleanup()
