from pyb import *
import time


# adxl345 registers
devid = 0x00
READWRITE_CMD = 0x80
MULTIBYTE_CMD = 0x40
devid_val = 0xE5
bw_rate = 0x2C
int_enable = 0x2E  # watermark = bit 1
data_format = 0x31  # spi bit, full_res bit, range bits, justify bit
power_ctl = 0x2D
dataX0 = 0x32
dataX1 = 0x33
dataY0 = 0x34
dataY1 = 0x35
dataZ0 = 0x36
dataZ1 = 0x37
offX = 0x1E
offY = 0x1F
offZ = 0x20
fifo_ctl = 0x38  # stream mode = 1 0 0 0 0 0 0 0

power_ctl_val = 0x00
bw_rate_val = 0xf
data_format_val = 0x10

n_bytes = 6

cs = Pin('X5', Pin.OUT)
cs.value(1)
spi = SPI(1, SPI.MASTER, baudrate=400000)

time.sleep(2)

cs.value(0)

spi.send(0x1E000)
test = spi.recv(1)
print("test1: ", test)
test &= 0x0
spi.send(test)
print("test new: ", spi.recv(1))


# buf = (int.from_bytes((spi.recv(1)), "little") & 0b01111111) << 1
buf = spi.recv(1)
print("liveID: ", buf, "\nExpected ID: ", devid_val)
cs.value(1)


# write
def spi_init(bw_rate, data_format, power_ctl):

    cs.value(0)
    # spi.send(bytearray((bw_rate, 0xf)))  # set baudrate to 100 Hz (0xf = 1111)
    # spi.send(bytearray((data_format, 0x0)))
    # spi.send(bytearray((power_ctl, 0x8)))  # turns measurement mode on (0x8 = 1000)


# read
def spi_read(start_byte, n_bytes):
    data = spi.recv(bytearray((start_byte, n_bytes)))
    data = spi.recv(bytearray(n_bytes))
    x = int.from_bytes(data[0:1], "little")
    y = int.from_bytes(data[2:3], "little")
    z = int.from_bytes(data[4:5], "little")
    cs.value(1)

    return x, y, z


def main():
    spi_init(bw_rate, data_format, power_ctl)

    i = 10
    j = 0
    while i >= 0:
        x, y, z = spi_read(dataX0, n_bytes)
        print("\nIteration: ", j)
        print("x = ", x)
        print("y = ", y)
        print("z = ", z)

        time.sleep(0.5)
        j += 1
        i -= 1


if __name__ == "_main_":
    main()
