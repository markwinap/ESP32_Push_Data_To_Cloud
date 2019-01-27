from machine import Timer
from machine import I2C
import binascii
import time
import machine
import network
import urequests

SSID = "INFINITUM3736_2.4"
PSW = "Maxpayne32"
APIGTW = "https://qmfrgy8wx6.execute-api.us-east-1.amazonaws.com/dev/diesel-monitor"
#I2C Configuration - DEFAULT PINS
i2c = I2C(0, I2C.MASTER, baudrate=100000)
#WIFI CONFIG
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect(SSID, auth=(network.WLAN.WPA2, PSW))
while not wlan.isconnected():
    time.sleep_ms(50)
print(wlan.ifconfig())
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
        self.timer_sonar = 10#Timer For Sonar I2C Scan 120
        self.timer_htpps = 60#Timer For Sigfox Push Data 730
        self.data = ""
        self.__alarm_sonar = Timer.Alarm(self._sonar_handler, self.timer_sonar, periodic=True)
        self.__alarm_https = Timer.Alarm(self._https_handler, self.timer_htpps, periodic=True)

    def _sonar_handler(self, alarm):
        i2c.writeto(0x70, 81)
        time.sleep(0.5)
        self.height = i2c.readfrom(0x70, 2)
        self.data += str(retInt(self.height)) + ","
        #DEBUG Uncomment To Print To Console Sonar Length In CM
        #print("%02d cm height" % retInt(self.height)) 
    def _https_handler(self, alarm):
        temp_l = self.data#Clone Data Arr
        self.data = ""#Clean Data Arr
        response =  urequests.request("POST", APIGTW, data = temp_l)
        response.close()
        temp_l = ""#Clean Temp Arr
clock = Clock()