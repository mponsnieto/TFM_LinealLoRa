#SENSOR D'HUMITAT HTU21D-F
import pycom
import time
from ustruct import unpack as unp
import math
from machine import Pin, I2C

HTU21D_HOLDMASTER         = 0x00
HTU21D_NOHOLDMASTER       = 0x10
HTU21D_MAX_MEASURING_TIME=100
mode=HTU21D_HOLDMASTER
I2C_ADDRESS=0X40
TEMP_ADDR=0XE3
HUM_ADDR=0XE5
i2c = I2C()
class SensorHumT:

    def __init__(self,i2c=None):
        pass

    def checkcrc(self,msb, lsb, crc):
        remainder = ((msb << 8) | lsb) << 8
        remainder |= crc
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def readTemperature(self):
        th=bytearray(1)
        tl=bytearray(1)
        crct=bytearray(1)


        #print("hum Adress: ",i2c.scan()) #64 dec es 0X40.
        #i2c.writeto_mem(I2C_ADDRESS, HUM_ADDR, buf *, addrsize=8)
        #self._htu_handler.send_command((HTU21D_TRIGGERTEMPCMD | mode) & 0xFF)
        #time.sleep(HTU21D_MAX_MEASURING_TIME/1000)
        #msb, lsb, chsum = self._htu_handler.read_bytes(3)
        #Llegir Temperatura
        i2c.writeto(I2C_ADDRESS,TEMP_ADDR) # write 2 bytes to slave 0x42, slave memory 0x10
        time.sleep(HTU21D_MAX_MEASURING_TIME/1000)
        th,tl,crct=i2c.readfrom(I2C_ADDRESS, 3) # receive 5 bytes from slave
        Stemp=(th<<8) | tl
        Stemp=Stemp & 0xFFFC
        Temp=-46.85+175.72*(Stemp/(2**16))
        okt=self.checkcrc(th,tl,crct)
        if okt == False: print("Error")
        else:
            print("Temp(ºC)",Temp)
            return Temp
    #Llegir Humitat

    def readHumidity(self):

        hh=bytearray(1)
        hl=bytearray(1)
        crch=bytearray(1)
        i2c.writeto(I2C_ADDRESS,HUM_ADDR) # write 2 bytes to slave 0x42, slave memory 0x10
        time.sleep(HTU21D_MAX_MEASURING_TIME/1000)
        hh,hl,crch=i2c.readfrom(I2C_ADDRESS, 3) # receive 5 bytes from slave
        Shum=(hh<<8) | hl
        Shum=Shum & 0xFFFC
        Hum=-6+125*(Shum/(2**16))
        okh=self.checkcrc(hh,hl,crch)
        if okh == False: print("Error")
        else:
            print("Hum (%)",Hum)
            return Hum # La conversió està al TTN per enviar paquets més petits



    # i2c.readfrom_mem_into(I2C_ADDRESS, HUM_ADDR,a)
    # i2c.readfrom_mem_into(I2C_ADDRESS, HUM_ADDR,b)
    # print(t1)
    # print(th)
