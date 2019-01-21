from machine import Timer
from machine import I2C
import binascii
import time

i2c = I2C(0, I2C.MASTER, baudrate=100000)

def retInt(hex):
  return int(binascii.hexlify(hex), 16)

class Clock:

    def __init__(self):
        self.height = 0
        self.__alarm = Timer.Alarm(self._sonar_handler, 1, periodic=True)

    def _sonar_handler(self, alarm):
        i2c.writeto(0x70, 81)
        time.sleep(0.5)
        self.height = i2c.readfrom(0x70, 2)
        print("%02d cm height" % retInt(self.height))

clock = Clock()