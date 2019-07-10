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
HT16K33_BLINK_OFF = 0
HT16K33_BLINK_2HZ = 1
HT16K33_BLINK_1HZ = 2
HT16K33_BLINK_HALFHZ = 3
HT16K33_CMD_BRIGHTNESS = 0xE0
HT16K33_OSCILATOR_ON = 0x21

initMatrix = False
matBuf = i2c.read(HT16K33_ADDRESS, 17)


class HT16K33:
    def __init__(self, i2c, address=HT16K33_ADDRESS):
        self.address = address
        self.temp = bytearray(1)
        self.buffer = bytearray(17)
        i2c.cmd(self.address, HT16K33_OSCILATOR_ON)
        i2c.cmd(self.address, HT16K33_BLINK_CMD |
                HT16K33_BLINK_DISPLAYON | (0 << 1))
        i2c.cmd(self.address, HT16K33_CMD_BRIGHTNESS | 0xF)

    def matrixShow(self):
        matBuf[0] = 0x00
        i2c.write(self.address, matBuf)
