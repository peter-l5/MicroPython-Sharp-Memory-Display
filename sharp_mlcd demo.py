# sharp memory display driver demo code
# this code is intended for a 400*240 pixel display
#
# this module copyright: 2026 Peter Lumb
# licence: MIT

__version__ = "0.4.005"
__repo__ = "https://github.com/peter-l5/MicroPython-Sharp-Memory-Display"

print("starting test")

# from machine import Pin, I2C
from machine import Pin, SPI
import sharp_mlcd

print("dir sharp_mlcd: ", dir(sharp_mlcd))
import gc
import sys
import time
import framebuf
import array

# time.sleep(5)

# basic test code SPI
spi0 = SPI(0, baudrate=2_000_000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
print(spi0)

display = sharp_mlcd.SharpMemoryDisplay(
    width=400, height=240, spi=spi0, cs=Pin(15, Pin.OUT)
)
print("display: ", dir(display))

display.clear()
print("display cleared")
time.sleep(2)

display.fill(0)
display.show()
print("display filled")
time.sleep(2)

display.fill(1)
display.show()
print("display filled")
time.sleep(2)

display.fill(0)
display.show()
print("display filled")
time.sleep(2)

display.text("SHARP MEMORY DISPLAY", 0, 0, 1)
display.text("driver", 0, 8, 1)
display.show(1, 16)
print("display filled")
time.sleep(3)

display.clear()