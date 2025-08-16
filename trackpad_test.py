import spidev
import RPi.GPIO as GPIO
import time

DR_PIN = 22
CS_PIN = 7   # keep wired to GPIO7 if you want to test with kernel CS; we'll also try manual CS below

GPIO.setmode(GPIO.BCM)
GPIO.setup(DR_PIN, GPIO.IN)
GPIO.setup(CS_PIN, GPIO.IN)  # don't drive it yet

spi = spidev.SpiDev()
spi.open(0, 1)  # CE1 (GPIO7)
# try a couple of modes and speeds
modes = [0b01, 0b11]
speeds = [500000, 1000000, 2000000]

try:
    for mode in modes:
        spi.mode = mode
        for s in speeds:
            spi.max_speed_hz = s
            print(f"\nSPI mode={mode:02b}, speed={s}")
            t0 = time.time()
            seen = 0
            while time.time() - t0 < 2.0:  # sample 2 seconds
                if GPIO.input(DR_PIN):
                    pkt = spi.readbytes(5)
                    print("DR=1 RAW:", [f"{b:02X}" for b in pkt])
                    seen += 1
                time.sleep(0.002)
            print("packets seen:", seen)
    print("\nDone. If you still only see FB.. packets, run the manual-CS test.")
except KeyboardInterrupt:
    pass
finally:
    spi.close()
    GPIO.cleanup()
