# driver for SHARP memory LCD displays
# based on CircuitPython module: `adafruit_sharpmemorydisplay`
# copyright: 2018 ladyada for Adafruit Industries
#
# this module copyright: 2026 peter-l5
# licence: MIT

"""
`adafruit_sharpmemorydisplay`
====================================================

A display control library for Sharp 'memory' displays

* Author(s): ladyada, peter-l5

Implementation Notes
--------------------

**Hardware:**

* `Adafruit SHARP Memory Display Breakout - 2.7 inch 240x400 Monochrome <https://www.adafruit.com/product/4694>`_
* `Adafruit SHARP Memory Display Breakout - 1.3 inch 144x168 Monochrome <https://www.adafruit.com/product/3502>`_
* `Adafruit SHARP Memory Display Breakout - 1.3 inch 96x96 Monochrome <https://www.adafruit.com/product/1393>`_

"""

__version__ = "0.4.005"
__repo__ = "https://github.com/peter-l5/MicroPython-Sharp-Memory-Display"
print("SHARP memory LCD display driver, version: ", __version__)

from machine import Pin
import gc
import sys
import time
from micropython import const

# import extended framebuffer if available)
try:
    import framebuf2 as framebuf

    _fb_variant = 2
except:
    import framebuf

    _fb_variant = 1
print(
    "SHARP memory LCD display driver, framebuf is:",
    ("MicroPython standard" if _fb_variant == 1 else "extended"),
)

# constants
_SHARPMEM_BIT_WRITECMD = const(0x80)
_SHARPMEM_BIT_VCOM = const(0x40)
_SHARPMEM_BIT_CLEAR = const(0x20)

# Precompute reversed bytes for fast bit reversal (LSB/MSB swap)
_REVERSE_BYTE = bytearray(256)
for i in range(256):
    b = i
    rev = 0
    for _ in range(8):
        rev = (rev << 1) | (b & 1)
        b >>= 1
    _REVERSE_BYTE[i] = rev


def reverse_bits(num: int) -> int:
    """Return the bit-reversed value of an 8-bit integer using lookup table."""
    return _REVERSE_BYTE[num & 0xFF]


class SharpMemoryDisplay(framebuf.FrameBuffer):
    """A driver for sharp memory displays, you can use any size but the
    full display must be buffered in memory!"""

    def __init__(self, width: int, height: int, spi: SPI, cs: Pin):
        self.spi = spi
        self.cs = cs
        self.cs.low()
        self.width = width
        self.height = height
        self.stride = width + 16

        # declare and initialise buffer with line numbers and trailing zeros
        self.width_b = (
            self.width // 8
        ) + 2  # allow for 1 leading and one trailing overhead bytes
        buffer_size = (
            self.width_b * height
        ) + 1  # extra byte avoids bug in earlier MicroPython versions
        self.displaybuffer = bytearray(buffer_size)
        self.displaybuffer_mv = memoryview(self.displaybuffer)
        for i in range(self.height):
            row_start = self.width_b * i
            self.displaybuffer[row_start] = reverse_bits(i + 1)
            self.displaybuffer[row_start + self.width_b - 1] = 0

        # set up sub-buffer memory view and initialise framebuffer
        self.screen_mv = memoryview(self.displaybuffer)[1:]
        super().__init__(
            self.screen_mv, self.width, self.height, framebuf.MONO_HLSB, self.stride
        )

        # initialise display buffer to white
        self.fill(1)

        # Set the vcom bit to a defined state
        self._vcom = True

    def show(self, start_line: int = 1, end_line: int = 240):
        _bufc = bytearray(1)
        start_line = max(1, start_line)
        end_line = min(end_line, self.height)

        # toggle the VCOM bit
        _bufc[0] = _SHARPMEM_BIT_WRITECMD
        if self._vcom:
            _bufc[0] |= _SHARPMEM_BIT_VCOM
        self._vcom = not self._vcom

        slice_from = (start_line - 1) * self.width_b
        slice_to = end_line * self.width_b
        print(range(slice_from, slice_to))
        self.cs.high()
        self.spi.write(_bufc)
        self.spi.write(self.displaybuffer_mv[slice_from:slice_to])
        self.spi.write(b"\x00")
        self.cs.low()

    def clear(self):
        _bufc = bytearray(2)
        _bufc[0] = _SHARPMEM_BIT_CLEAR
        _bufc[1] = 0
        self.cs.high()
        self.spi.write(_bufc)
        self.cs.low()
