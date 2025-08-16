import spidev
import RPi.GPIO as GPIO
import time

# Pin definitions
DR_PIN = 22  # Data Ready
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, device 0 (SS pin GPIO 7 mapped to CE0)
spi.max_speed_hz = 1000000  # 1 MHz
spi.mode = 0b00

def read_trackpad():
    # Wait for DR to go low (data ready)
    while GPIO.input(DR_PIN):
        time.sleep(0.001)
    
    # TM040040 typically sends 4 bytes: Status, X_H, X_L, Y_H, Y_L
    raw_data = spi.readbytes(5)
    
    status = raw_data[0]
    x = (raw_data[1] << 8) | raw_data[2]
    y = (raw_data[3] << 8) | raw_data[4]
    
    return status, x, y

try:
    while True:
        status, x, y = read_trackpad()
        print(f"Status={status:02X}, X={x}, Y={y}")
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    spi.close()
    GPIO.cleanup()
