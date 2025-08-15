import spidev
import time

# --- Setup SPI ---
spi = spidev.SpiDev()
spi.open(0, 0)           # bus 0, device 0 (adjust if needed)
spi.max_speed_hz = 1000000  # 1 MHz
spi.mode = 0b01           # CPOL=0, CPHA=1 (check datasheet)
spi.bits_per_word = 8

# --- Example: read a register ---
def read_register(reg_addr, length=1):
    """
    Read 'length' bytes from a given register.
    TM040040 may require a write phase before read.
    """
    # Many SPI devices require MSB=0 for read/write distinction.
    # Adjust reg_addr according to datasheet if needed.
    write_data = [reg_addr & 0x7F]  # example: clear MSB for read
    spi.xfer2(write_data)           # send address
    time.sleep(0.001)               # small delay
    return spi.readbytes(length)     # read bytes

# --- Example: main loop ---
try:
    while True:
        # Example: read 4 bytes from register 0x00
        data = read_register(0x00, 4)
        print("Trackpad data:", data)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    spi.close()
