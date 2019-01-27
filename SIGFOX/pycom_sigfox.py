# print Sigfox Device ID
# b'004d58b1' # print(binascii.hexlify(sigfox.id()))
# b'03fdb4b54fc6c872' # print(binascii.hexlify(sigfox.pac()))
# RCZ1 – Europe
# RCZ2 – US
# RCZ3 – TBD
# RCZ4 – Australia/New Zealand
# Sigfox Limits 140 Messages Day OF Max Data Len of 12 Bytes

from machine import Timer
from machine import I2C
import binascii
import time
import machine
from network import Sigfox
import socket
#I2C Configuration - DEFAULT PINS
i2c = I2C(0, I2C.MASTER, baudrate=100000)
#SIGFOX CONFIG 
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ2)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)

def retInt(hex):#HELPER FUNCTION Byte Array to Int
  return int(binascii.hexlify(hex), 16)

def sendData(arr):
    try:
        s.send(bytes(arr))
    except:
        machine.reset()
def getSenorData():
    try:
        s.send(bytes(arr))
    except:
        machine.reset()
class Clock:
    def __init__(self):
        self.height = 0
        self.timer_sonar = 60 * 2#Timer For Sonar I2C Scan 120
        self.timer_sigfox = (60 * 12) + 10#Timer For Sigfox Push Data 730
        self.data = []
        self.__alarm_sonar = Timer.Alarm(self._sonar_handler, self.timer_sonar, periodic=True)
        self.__alarm_sigfox = Timer.Alarm(self._sigfox_handler, self.timer_sigfox, periodic=True)

    def _sonar_handler(self, alarm):
        i2c.writeto(0x70, 81)
        time.sleep(0.5)
        self.height = i2c.readfrom(0x70, 2)
        self.data.append(self.height[0])
        self.data.append(self.height[1])
        #DEBUG Uncomment To Print To Console Sonar Length In CM
        #print("%02d cm height" % retInt(self.height)) 
    def _sigfox_handler(self, alarm):
        temp_l = self.data.copy()#Clone Data Arr
        self.data.clear()#Clean Data Arr
        if len(temp_l) > 12:#Data Ar Len > 12, Remove Older Bytes
            while (len(temp_l) > 12):
                temp_l.pop(0)#Remove First Byte from Arr
            sendData(temp_l)
        else:
            sendData(temp_l)
        temp_l.clear()#Clean Temp Arr

clock = Clock()