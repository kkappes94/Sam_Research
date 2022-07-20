from pyb import SPI, Pin

spi = SPI(1, SPI.CONTROLLER, baudrate=400000)
cs = Pin('X5', Pin.OUT)
cs.value(1)

# adxl345 registers
bw_rate = 0x2C
int_enable = 0x2E # watermark = bit 1
data_format = 0x31 # spi bit, full_res bit, range bits, justify bit
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
fifo_ctl = 0x38 # stream mode = 1 0 0 0 0 0 0 0

# write
cs.value(0)
spi.send(bw_rate | 0xf) # set baudrate to 100 Hz
spi.send(data_format | 0)
spi.send(power_ctl | 0x8) # turns measurement mode on

# read
data = spi.recv(8)
x = int.from_bytes(data[0:1],"little")
y = int.from_bytes(data[2:3],"little")
z = int.from_bytes(data[4:5],"little")
cs.value(1)

print("x = ", x)
print("y = ", y)
print("z = ", z)