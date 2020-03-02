import time
import pycom
import machine
from machine import Pin, I2C
from ustruct import unpack as unp
import Camera as cam
import SensorHumT as sensH
import MCP9808 as adafruit_mcp9808
from bmp085 import BMP085
import HumedadSuelo as HS
import Comunication as com
import QAire as QA
import HPMA115S0 as pma
import ubinascii
import ustruct

com=com.Comunication()
com.start_LoraRaw()

# initialize `P9` in gpio mode and make it an output
p_out = Pin('P12', mode=Pin.OUT)

i2c = I2C()
sensorQAire=QA.QAire('P20','P21')
sensorHSol=HS.HumitatSol('P19')
SensorHT=sensH.SensorHumT()
mcp = adafruit_mcp9808.MCP9808(i2c)
cam = cam.Camera(i2c)
bmp = BMP085(i2c)
pma=pma.HPMA1150S0()

## Initialize time
rtc = machine.RTC()
#(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
rtc.init((2020, 02, 28, 11,01))
