import time
from machine import Pin, I2C
import pycom
import machine
from ustruct import unpack as unp
import math
# import Camera as cam
# import SensorHumT as sensH
# import MCP9808 as adafruit_mcp9808
# from bmp085 import BMP085
# import HumedadSuelo as HS
import Comunication as com
import QAire as QA
from network import LoRa
import socket
import ubinascii
import ustruct
from crypto import AES
import crypto

# i2c = I2C()
# sensorQAire=QA.QAire('P20','P21')
# sensorHSol=HS.HumitatSol('P19')
# SensorHT=sensH.SensorHumT()
# mcp = adafruit_mcp9808.MCP9808(i2c)
# cam = cam.Camera(i2c)
# bmp = BMP085(i2c)
com=com.Comunication()
# bmp.oversample=2
# bmp.sealevel=1013.25

id=ubinascii.hexlify(machine.unique_id()).decode('utf-8') #'3c71bf8775d4'
print("device id: ",id)
id_aux=ustruct.pack('>Q',int(id,16)) #long long: 8 bytes

# ## Initialize time
# rtc = machine.RTC()
# #(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
# rtc.init((2019, 10, 16, 9, 22))
