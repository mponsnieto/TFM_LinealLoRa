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
        #Delete data's contents
        f = open('data_HTU.txt', 'w')
        f.close()
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

    def saveFile(self,T,rtc):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) Temperature [ºC]
        Example: 15/10/2019 13:21:31 26.4
        '''
        #Write the image temp in data.txt
        f = open('data_HTU.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],T))
        f.close()
        return
