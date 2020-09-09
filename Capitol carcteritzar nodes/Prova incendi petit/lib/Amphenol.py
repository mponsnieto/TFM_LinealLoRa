from machine import UART

class Amphenol:
    def __init__(self):
        self.uart = UART(1,9600) #USE P2 P3 , keep UART 0 for usb connection
        self.uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters
        pass

    def readDust(self):
        i=0
        while self.uart.any() <= 32:
         if self.uart.read(1)==b'B': #hex 0x42
            data=self.uart.read(32)
            print("Data: ", data)
        return
