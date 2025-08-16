import spidev
import RPi.GPIO as GPIO
import time

# Pin definitions
DR_PIN = 22       # Data Ready
CE_PIN = 7        # Chip Select for trackpad
GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CE_PIN, GPIO.OUT)
GPIO.output(CE_PIN, GPIO.HIGH)  # CE inactive

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # Use any bus/device; CE will be manual
spi.max_speed_hz = 500000  # 500 kHz is safer
spi.mode = 0b01

def read_trackpad():
    # Pull CE low to start SPI transaction
    GPIO.output(CE_PIN, GPIO.LOW)
    
    # Send read command (0x00 is typical; check your module datasheet)
    # TM040040 usually responds with 5 bytes: Status, X_H, X_L, Y_H, Y_L
    raw_data = spi.xfer2([0x00]*5)
    
    # Release CE
    GPIO.output(CE_PIN, GPIO.HIGH)
    
    status = raw_data[0]
    x = (raw_data[1] << 8) | raw_data[2]
    y = (raw_data[3] << 8) | raw_data[4]
    
    return status, x, y

try:
    while True:
        # Optionally, check DR before reading
        if GPIO.input(DR_PIN) == 0:
            status, x, y = read_trackpad()
            print(f"Status={status:02X}, X={x}, Y={y}")
        else:
            print("No touch detected")
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    spi.close()
    GPIO.cleanup()
