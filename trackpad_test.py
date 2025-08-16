import spidev
import RPi.GPIO as GPIO
import time

# Pin definitions
DR_PIN = 22  # Data Ready
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 1)  # Bus 0, device 1 → CE1 (GPIO 7)
spi.max_speed_hz = 100000  # 100 kHz
spi.mode = 0b00

def read_trackpad(timeout=1.0):
    start = time.time()
    # Wait for DR to go low (data ready) with timeout
    while GPIO.input(DR_PIN):
        if time.time() - start > timeout:
            return None, None, None
        time.sleep(0.001)
    
    # Read 5 bytes: Status, X_H, X_L, Y_H, Y_L
    raw_data = spi.readbytes(5)
    
    status = raw_data[0]
    x = (raw_data[1] << 8) | raw_data[2]
    y = (raw_data[3] << 8) | raw_data[4]
    
    return status, x, y

try:
    while True:
        status, x, y = read_trackpad()
        if status is not None:
            print(f"Status={status:02X}, X={x}, Y={y}")
        else:
            print("No data (DR never went low)")
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    spi.close()
    GPIO.cleanup()
