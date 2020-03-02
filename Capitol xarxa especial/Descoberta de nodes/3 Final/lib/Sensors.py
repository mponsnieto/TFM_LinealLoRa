import Camera as cam
import SensorHumT as sensH
import MCP9808 as adafruit_mcp9808
from bmp085 import BMP085
import HumedadSuelo as HS
import QAire as QA
from machine import Pin, I2C
from ustruct import unpack as unp
import ustruct
from machine import Timer
import math

class Comunication:
    def __init__(self):
        i2c = I2C()
        self.sensorQAire=QA.QAire('P20','P21')
        self.sensorHSol=HS.HumitatSol('P19')
        self.SensorHT=sensH.SensorHumT()
        self.mcp = adafruit_mcp9808.MCP9808(i2c)
        #cam = cam.Camera(i2c)
        self.bmp = BMP085(i2c)
        self.bmp.oversample=2
        self.bmp.sealevel=1013.25
        pass

  def llegirSensors(self):
          #Sensor PT BMP085
      temp = bmp.GetTemperature
      packet_tbmp = ustruct.pack('f',temp)
      dataBMP="Temp: %0.2f *C" % (temp)
      print(dataBMP)
      time.sleep(0.3)
      temp=int(temp)

      # #Sensor T MCP
      time.sleep(0.3)
      tempC = mcp.GetTemperature
      packet_tempC = ustruct.pack('f',tempC)
      dataMCP='Temperature: {} C '.format(tempC)
      print(dataMCP)
      tempC=int(tempC)
      time.sleep(0.3)

      #Sensor HS
      val,dry,humid,inWater=sensorHSol.CalcularHumitat()
      dhi=dry+humid*2+inWater*3
      packet_dhi = ustruct.pack('b',dhi)
      packet_val = ustruct.pack('H',val)
      # packet_dry = ustruct.pack('f',dry)
      # packet_humid = ustruct.pack('f',humid)
      # packet_inWater = ustruct.pack('f',inWater)
      dataHS='Humitat del sol: {} , Humit={}, sec={}, Aigua={}'.format(val,humid,dry,inWater)
      print(dataHS)
      print("dhi es  ",dhi)
      val=int(val)
      #Sensor QAire
      dustDensity=sensorQAire.CalculateDust()
      time.sleep(1)
      dust='DustDensity: {} ug/m3'.format(dustDensity)
      print("DustDensity: ",dustDensity," ug/m3")
      packet_dust = ustruct.pack('f',dustDensity)
      dustDensity=int(dustDensity)
      #Càmera
      # Temp=cam.readTemp
      # print("T from thermistor= %0.2f *C" % (Temp))
      # T=cam.readPixels
      # print("Image readen pixel by pixel in *C")
      # for i in range(8): print(T[i])
      # time.sleep(periode)
      # packet_TCam = ustruct.pack('f',Temp)
      #Sensor HT
      T=SensorHT.readTemperature()
      time.sleep(0.3)
      packet_Tht = ustruct.pack('f',T)
      H=SensorHT.readHumidity()
      time.sleep(0.3)
      packet_Hht = ustruct.pack('H',round(H*100))
      T=int(T)
      H=int(H)
      #list=[dustDensity,tempC,T,H,temp,val,dhi]
      a=" "
      list=str(dustDensity)+a+str(tempC)+a+str(T)+a+str(H)+a+str(temp)+a+str(val)+a+str(dhi)
      data=[packet_dust,packet_tempC,packet_Tht,packet_Hht,packet_tbmp,packet_val,packet_dhi]
      return(packet_dust+packet_tempC+packet_Tht+packet_Hht+packet_tbmp+packet_val+packet_dhi,list)
