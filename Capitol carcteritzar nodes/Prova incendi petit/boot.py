import time
from machine import Pin, I2C
import pycom
import machine
from ustruct import unpack as unp
import math
import Camera as cam
import SensorHumT as sensH
import MCP9808 as adafruit_mcp9808
from bmp085 import BMP085
import Amphenol as QA2
import HumedadSuelo as HS
# import Comunication as com
import QAire as QA
# from network import LoRa
# import socket
# import ubinascii
# import ustruct
# from crypto import AES
# import crypto

i2c = I2C()
sensorAmphenol=QA2.Amphenol()
sensorQAire=QA.QAire('P20','P21')
sensorHSol=HS.HumitatSol('P19')
SensorHT=sensH.SensorHumT()
mcp = adafruit_mcp9808.MCP9808(i2c)
cam = cam.Camera(i2c)
bmp = BMP085(i2c)
bmp.oversample=2
bmp.sealevel=1013.25

# ## Initialize time
rtc = machine.RTC()
#(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
rtc.init((2020, 09, 09, 0, 0))
