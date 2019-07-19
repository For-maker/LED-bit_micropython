# 在这里写上你的代码 :-)
from microbit import sleep, i2c
import HT16K33
LED1 = HT16K33.Matrix16x8(i2c)
LED1.pixel(7, 7, 255)
LED1.show()
