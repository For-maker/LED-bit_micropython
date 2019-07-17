# Copyright (c) 2019, 五丝菜卷/wusicaijuan
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from microbit import i2c

# HT16K33 commands
HT16K33_ADDRESS = 0x70
HT16K33_BLINK_CMD = 0x80
HT16K33_BLINK_DISPLAYON = 0x01
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_OSCILATOR_ON = 0x21

class HT16K33(object):
    """The base class for all HT16K33-based backpacks and wings."""

    def __init__(self, i2c, address=HT16K33_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.temp = bytearray(1)
        self.buffer = bytearray(17)
        self.buffer[0] = 0x00
        self.fill(0)
        self.write_cmd(HT16K33_OSCILATOR_ON)
        self.blink_rate(0)
        self.brightness(15)

    def write_cmd(self, byte):
        """Send a command."""
        self.temp[0] = byte
        self.i2c.write(self.address, self.temp)

    def blink_rate(self, rate=None):
        """Get or set the blink rate."""
        if rate is None:
            return self.blink_rate
        rate = rate & 0x02
        self.blink_rate = rate
        self.write_cmd(HT16K33_BLINK_CMD |
                        HT16K33_BLINK_DISPLAYON | rate << 1)

    def brightness(self, brightness):
        """Get or set the brightness."""
        if brightness is None:
            return self.brightness
        brightness = brightness & 0x0F
        self.brightness = brightness
        self.write_cmd(HT16K33_CMD_BRIGHTNESS | brightness)

    def show(self):
        """Actually send all the changes to the device."""
        self.i2c.write(self.address, self.buffer)

    def fill(self, color):
        """Fill the display with given color."""
        fill = 0xff if color else 0x00
        for i in range(16):
            self.buffer[i + 1] = fill

    def pixel(self, x, y, color=None):
        """Set a single pixel in the frame buffer to specified color."""
        mask = 1 << x
        if color is None:
            return bool((self.buffer[y + 1] | self.buffer[y + 2] << 8) & mask)
        if color:
            self.buffer[y * 2 + 1] |= mask & 0xff
            self.buffer[y * 2 + 2] |= mask >> 8
        else:
            self.buffer[y * 2 + 1] &= ~(mask & 0xff)
            self.buffer[y * 2 + 2] &= ~(mask >> 8)


class Matrix16x8(HT16K33):
    """The double matrix."""

    def pixel(self, x, y, color=None):
        """Set a single pixel in the frame buffer to specified color."""
        if not 0 <= x <= 15:
            return
        if not 0 <= y <= 7:
            return
        if x >= 8:
            x -= 8
            y += 8
        return super().pixel(y, x, color)


class Matrix8x8(HT16K33):
    """The single matrix."""

    def pixel(self, x, y, color=None):
        """Set a single pixel in the frame buffer to specified color."""
        if not 0 <= x <= 7:
            return
        if not 0 <= y <= 7:
            return
        x = (x - 1) % 8
        return super().pixel(x, y, color)


class Matrix8x8x2(HT16K33):
    """The bi-color matrix."""

    def pixel(self, x, y, color=None):
        """Set a single pixel to specified color."""
        if not 0 <= x <= 7:
            return
        if not 0 <= y <= 7:
            return
        if color is not None:
            super().pixel(y, x, (color & 0x01))
            super().pixel(y + 8, x, (color >> 1) & 0x01)
        else:
            return super().pixel(y, x) | super().pixel(y + 8, x) << 1

    def fill(self, color):
        """Fill the display with given color."""
        fill1 = 0xff if color & 0x01 else 0x00
        fill2 = 0xff if color & 0x02 else 0x00
        for i in range(8):
            self.buffer[i * 2] = fill1
            self.buffer[i * 2 + 1] = fill2
