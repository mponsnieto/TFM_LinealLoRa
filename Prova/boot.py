import time
import pycom
import machine
from machine import Pin, I2C
from ustruct import unpack as unp
import math
import Camera as cam
import SensorHumT as sensH
import MCP9808 as adafruit_mcp9808
from bmp085 import BMP085
import HumedadSuelo as HS
import Comunication as comu
import QAire as QA
import ubinascii
import ustruct

counter=0
id=ubinascii.hexlify(machine.unique_id()).decode('utf-8') #'3c71bf8775d4'
print("device id: ",id)
id_aux=ustruct.pack('>Q',int(id,16)) #long long: 8 bytes

# initialize `P9` in gpio mode and make it an output
#p_out = Pin('P7', mode=Pin.OUT)

com=comu.Comunication()
