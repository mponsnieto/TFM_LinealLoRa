import time
from machine import Pin, I2C

class Camera:

    THERMISTOR_CONVERSION = 0.0625 #1 LSB has 12 bit resolution which is equivalent to 0.0625°C
    PIXEL_CONVERSION = 0.25 #1 LSB has 12 bit resolution (11 bit + sign) which is equivalent to 0.25°C
    CAM_ADDRESS=0x69
    T_LLINDAR=50
    POWER_MODE=0x00
    def __init__(self,i2c=None):
        if i2c is None:
            raise ValueError("The I2C bus must be specified")
        else:
            self._cam_i2c = i2c
            self.buf = bytearray(2)
        #Delete data's contents
        f = open('data_cam.txt', 'w')
        f.close()
        #Delete data's contents
        f = open('data_cam_images.txt', 'w')
        f.close()

    def gotosleep(self):
        self._cam_i2c.writeto_mem(self.CAM_ADDRESS, self.POWER_MODE, 0x10, addrsize=8)
        print("go to sleep")

    def SoftReset(self):
        self._cam_i2c.writeto_mem(self.CAM_ADDRESS, 0x01, 0x3F, addrsize=8)

    def wakeup(self):
        self._cam_i2c.writeto_mem(self.CAM_ADDRESS, self.POWER_MODE, 0x00, addrsize=8)
        print("good morning")
        time.sleep(1)

    def checkAlarm(self,temp,temp_ant,templist,templist_ant):
        '''
        If thermistor or image temp is higher than a threshold and higher than the previous -> alarm
         temp=25
         temp_ant=20
         templist=[[1, 2, 3], [55, 5, 6]]
         templist_ant=[[5, 2, 3], [4, 5, 6]]
        '''
        alarma=False
        if temp > self.T_LLINDAR and temp > temp_ant:
            alarma= True
        #Recórrer matriu de T i mirar si han augmentat i són majors que el llindar
        else:
            for i in range(8):
                for j in range(8):
                    if templist[i][j]>templist_ant[i][j] and templist[i][j]>self.T_LLINDAR:
                        alarma=True
        return alarma



    def _ConvertirValor(self,val,val2):
        '''
        Convert msb & lsb to obtain the correct value of Temp.
        '''
        valor = (val << 8) | val2
        mask=0b00001000
        mask2=0b00000111
        mask2 = (mask2 << 8) | 0b11111111
        sign = mask & val # Check sign bit
        if sign==0:
           #Positive number
           return valor
        else:
            #Convert to negative
           valor= valor & mask2
           valor=valor*-1
        return valor

    @property
    def readTemp(self):
        '''
        Temperature from thermistor in degree C.
        '''
        self.wakeup()
        tl=bytearray(1) #Lower part of Temp saved in 0x0E register
        th=bytearray(1) #High part of Temp saved in 0x0F register
        self._cam_i2c.readfrom_mem_into(self.CAM_ADDRESS, 0x0E, tl)
        self._cam_i2c.readfrom_mem_into(self.CAM_ADDRESS, 0x0F, th)
        #self.gotosleep()
        raw=self._ConvertirValor(th[0],tl[0])
        return raw*self.THERMISTOR_CONVERSION

    @property
    def readPixels(self):
        '''
        Method for read the temperature pixel-by-pixel.
        Returns a complete image (8x8).
        The address register are from 0x80 to 0xFF
         '''
        self.wakeup()
        txl=bytearray(1)
        txh=bytearray(1)
        T = [[0]*8 for _ in range(8)] #Create a 8x8 array
        row=0
        col=0
        for x in range(64): #Loop for explore from de 0x80 Adress to 0xFF (8x8 pixels x 2:MSB,LSB)
            self._cam_i2c.readfrom_mem_into(self.CAM_ADDRESS, x*2+0x80, txl)
            self._cam_i2c.readfrom_mem_into(self.CAM_ADDRESS, x*2+0x81, txh)

            raw=self._ConvertirValor(txh[0],txl[0])
            Tx=raw*self.PIXEL_CONVERSION
            T[row][col]=Tx
            col=col+1
            if col==8:
                col=0
                row=row+1
        #self.gotosleep()
        return T

    def saveFile(self,image,T,rtc):
        '''
        Format of the data: 8x8 with sep= ','
        Example:
             T11,T12,...,T18
             T21,T22,...,T28
                    .
                    .
                    .
             T81,T82,...,T88
         '''
        str1=""
        for i in range(8):
            for j in range(8):
                if (j==0 and i==0):
                    str1=str1+str(image[i][j])
                else:
                    str1=str1+","+str(image[i][j])

        #Write the image temp in data.txt
        f = open('data_cam_images.txt', 'a')
        f.write("{}/{}/{} {}:{}:{}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
        f.write(str1)
        f.write("\n")
        f.close()

        #Delete data's contents
        f = open('data_cam.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],T))
        f.close()
