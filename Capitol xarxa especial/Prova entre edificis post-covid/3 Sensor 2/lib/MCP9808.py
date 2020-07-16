import time

class MCP9808:
    #Adress I2C
    MCP_ADDRESS = 0x18
    TA_Register= 0x05
    Config_Register=0x01

    def __init__(self,i2c=None):
        if i2c is None:
            raise ValueError("The I2C bus must be specified")
        else:
            self._mcp_i2c = i2c
        self.buf = bytearray(2)
        self._mcp_i2c.readfrom_mem_into(self.MCP_ADDRESS, self.TA_Register, self.buf,addrsize=8)


    def gotosleep(self):
        self._mcp_i2c.readfrom_mem_into(self.MCP_ADDRESS,self.Config_Register,self.buf,addrsize=8)
        if (self.buf[1]&0xC0 == 0x00): #If not locked, go to sleep
            self._mcp_i2c.writeto_mem(self.MCP_ADDRESS,self.Config_Register,self.buf[0]|0x01,addrsize=8)
            print("Go to sleep")

    
    def wakeup(self):
        self._mcp_i2c.writeto_mem(self.MCP_ADDRESS,self.Config_Register,self.buf[0]&0xFE,addrsize=8)
        print("Wake")

    @property
    def GetTemperature(self):
        '''
        Temperature in degree C.
        '''
        self.wakeup()
        #Read T register, the adress is 0x05
        self._mcp_i2c.readfrom_mem_into(self.MCP_ADDRESS, self.TA_Register, self.buf,addrsize=8)
        time.sleep(0.5)

        # Clear flags from the value
        sign = self.buf[0] & 0x10
        upperTemp = self.buf[0] & 0x0F
        lowerTemp =self.buf[1]

        if sign & 0x1 == 0x1: #Si signo negativo
             return (256- ( (upperTemp * 16) + (lowerTemp / 16.0)))
        self.gotosleep()
        return ( (upperTemp *16.0 ) + (lowerTemp/16.0))
