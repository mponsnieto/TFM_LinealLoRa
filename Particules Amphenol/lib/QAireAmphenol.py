from machine import UART

class QAireAmphenol:
    def __init__(self):
        self.uart = UART(1, 9600)
        pass
    def readDus(self):
        self.uart.read(b'\x42\x4D\x86\x00\x00\x00\x00\x00\x79') # This is what should trigger the measure
uart.read(9) #b'\xff\x86\x01\xecF\x00\x00\x00G' #This is the answer
