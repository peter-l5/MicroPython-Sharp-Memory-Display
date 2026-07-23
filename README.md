# MicroPython - Sharp Memory Display driver

MicroPython driver for Sharp Memory Displays.

This driver was derived from the Adafruit CircuitPython version - [Adafruit_CircuitPython_SharpMemoryDisplay](https://github.com/adafruit/Adafruit_CircuitPython_SharpMemoryDisplay) - made by @ladyada and others. It has been enhanced as follows: 
* the speed of display updates has been significantly improved and memory use reduced
* a `clear()` method has been added to trigger the built-in hardware screen clear 

## Features and performance

For the Adafruit 400x240 display using a SPI connection at 2 MHz from  a Raspberry Pi Pico 2, full screen updates are possible in around 65 ms. 

The driver builds in the facility to use the extended framebuffer methods **`large_text()`**, **`triangle()`** and **`circle()`** methods in the MicroPython FrameBuffer extension [framebuf2](https://github.com/peter-l5/framebuf2). 

## Important
To prevent potential permanent burn-in on the display the polarity must be reversed at least every 2 hours. This can be achieved by refreshing the display with the `show()` method. See display datasheet and application note for further information.

## Display connection

The display has an SPI interface, connections for SCLK, MOSI, CS are required.

## Usage

The [module code](/sharp_mlcd.py) should be uploaded to the Raspberry Pico Pi (or other Microcontroller running MicroPython). The large font, triangle and circles extension is added by additionally uploading the `framebuf2.py` module code. (See [framebuf2](https://github.com/peter-l5/framebuf2).) 

## Classes

The module includes the class `SharpMemoryDisplay`. 

syntax:
```
display = sharp.SharpMemoryDisplay(
    width, 
    height, 
    spi,
    cs
)
```
- `width` (default 400) and `height` (default 240) define the size of the display
- `spi` is an SPI object. The SCL (clock) and MOSI (data) pins must be defined. MISO is not used.
- `cs` is a GPIO Pin object for Chip Select

## Methods and Properties

In addition to all MicroPython's framebuffer drawing methods, the following methods and properties are available for controlling the display:

**`show(startline, endline)`** - this method updates the display from the framebuffer. Partial updates for rows between a  **`startline`** and an **`endline`** are possible and are faster than a full screen update. Omit both these parameters to update the whole display.

**`clear()`** - this method clears the display (to colour 1). It does not change the contents of the framebuffer. To clear the framebuffer to white as well, call the framebuffer method `fill(1)`. 

### Example usage
```
    from machine import Pin, SPI
    import sharp

    spi0 = SPI(0, baudrate=2_000_000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    display = sharp_mlcd.SharpMemoryDisplay(400, 240, spi0, cs=Pin(15, Pin.OUT))

    display.fill(0)
    display.text('SHARP MEMORY DISPLAY', 0, 0, 1)
    display.text('driver', 0, 8, 1)
    display.show()
```
See [demo example](/sharp_mlcd demo.py) for more details. (The example code was written for 400x240 displays.)

## Tested displays 

This driver has been tested with a Raspberry Pi Pico 2 W running MicroPython 1.28.0 and an [Adafruit 400x240 display](https://www.adafruit.com/product/4694). It should work with other Adafruit Sharp Memory Display breakout boards. 

## Version notes

#### version 0.4.005
- initial commit
- improves speed and memory usage vs Adafruit driver by adding the display line numbers and trailing zero bytes to the framebuffer and then using a sub-framebuffer for the display content. Thus avoiding slow and memory-costly extensions to a bytearray used in the Adafruit driver for updating the display
- possibility for partial screen updates added
- hardware-based screen `clear()` method included

## Collaboration

Suggestions for improvements and pull requests are welcome.

## References

[Adafruit SHARP memory display breakouts documentation](https://learn.adafruit.com/adafruit-sharp-memory-display-breakout) (links to datasheets can be found here)

[Application Note: Sharp Memory LCDs: Theory,
Interfacing, and Programming](https://www.mikrocontroller.net/attachment/433460/Memory_LCD_Theory__Programming__and_Interfaces.pdf)
