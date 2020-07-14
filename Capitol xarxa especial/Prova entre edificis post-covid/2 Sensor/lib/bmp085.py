from ustruct import unpack as unp
import math
import time


# BMP085 library
class BMP085():
    #Calibration params
    AC1=0
    AC2=0
    AC3=0
    AC4=0 #UNSIGNED SHORT
    AC5=0 #UNSIGNED SHORT
    AC6=0 #UNSIGNED SHORT
    B1=0
    B2=0
    MB=0
    MC=0
    MD=0
    B5 = 0
    #To read T and P
    UT=bytearray(2)
    UP=bytearray(3)
    #Adress I2C
    BMP_ADDRESS = 0x77


    def __init__(self,i2c=None):
        if i2c is None:
            raise ValueError("The I2C bus must be specified")
        else:
            self._bmp_i2c = i2c

        (self.AC1, self.AC2, self.AC3, self.AC4, self.AC5, self.AC6,
         self.B1, self.B2, self.MB, self.MC, self.MD) = \
            unp('>hhhHHHhhhhh',
                self._bmp_i2c.readfrom_mem(self.BMP_ADDRESS, 0xAA, 22))





        #Reference for Altitude
        self._baseline = 1013.25
        # #Oversample can be 0, 1, 2 o 3
        self._oversample = 0 #antes era un 3

    def getCalibParams(self):
        '''
        Returns a list of all calibration params readen
        '''
        if AC1!=0:
            return [self.AC1, self.AC2, self.AC3, self.AC4, self.AC5,
                self.AC6, self.B1, self.B2, self.MB, self.MC, self.MD,
                self._oversample]
        else:
            return [0,0,0,0,0,0,0,0,0,0,0,0]
            print("Error reading calib parameters")

    @property
    def sealevel(self):
        return self._baseline

    @sealevel.setter
    def sealevel(self,value):
        if 300 < value < 1200:  # just ensure some reasonable value
            self._baseline = value

    @property
    def oversample(self):
        print("Hi")
        return self._oversample

    @oversample.setter
    def oversample(self,value):
        if value in range(4):
            self._oversample = value
        else:
            print("Oversample can only be 0, 1, 2 or 3, using 3 instead")
            self._oversample = 0

    @property
    def GetTemperature(self):
        '''
        Temperature in degree C.
        '''
        #Read T register
        self._bmp_i2c.writeto_mem(self.BMP_ADDRESS, 0xF4, 0x2E, addrsize=8)
        time.sleep(0.5)
        self._bmp_i2c.readfrom_mem_into(self.BMP_ADDRESS, 0xF6, self.UT)
        time.sleep(0.5)

        X1 = ((unp(">H", self.UT)[0] -self. AC6) * self.AC5) >> 15
        X2 = (self.MC << 11) // (X1 + self.MD)
        self.B5 = X1 + X2
        return ((self.B5 + 8) >> 4) / 10.0  #Have we to add a -1.5???

    @property
    def GetPressure(self):
        '''
        Pressure in hPa.
        '''
        temperature=self.GetTemperature  # Get values for temperature AND pressure

        #Read P register
        self._bmp_i2c.writeto_mem(self.BMP_ADDRESS, 0xF4, 0x34, addrsize=8)
        time.sleep(0.5)
        self._bmp_i2c.readfrom_mem_into(self.BMP_ADDRESS, 0xF6, self.UP)

        UP = (((self.UP[0] << 16) + (self.UP[1] << 8) + self.UP[2]) >>
              (8 - self._oversample))
        B6 = self.B5 - 4000
        X1 = (self.B2 * ((B6 * B6) >> 12)) >> 11
        X2 = (self.AC2 * B6) >> 11
        B3 = (((self.AC1 * 4 + X1 + X2) << self._oversample) + 2) >> 2
        X1 = (self.AC3 * B6) >> 13
        X2 = (self.B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self._oversample)
        p = (B7 * 2) // B4
        X1 = (((p >> 8) * (p >> 8)) * 3038) >> 16
        X2 = (-7357 * p) // 65536
        return (p + (X1 + X2 + 3791) // 16) / 100

    @property
    def GetAltitude(self):
        '''
        Altitude in m.
        '''
        try:
            p = 44330 * (1.0 - math.pow(self.GetPressure/
                                        self._baseline, 0.1903))
        except:
            p = 0.0
        return p
