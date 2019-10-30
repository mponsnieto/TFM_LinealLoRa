from machine import UART
import time

# this uses the UART_1 default pins for TXD and RXD (``P3`` and ``P4``)
uart = UART(1, baudrate=9600)

class HPMA1150S0:
    def __init__(self):
        Fan=True
        self.startFan()
        pass

    def stopFan(self):
        print("Fan OFF")
        self.Fan=False
        uart.write(b'\x68\x01\x02\x95')
        data=uart.readall()
        return

    def startFan(self):
        print("Fan ON")
        self.Fan=True
        uart.write(b'\x68\x01\x01\x96')
        time.sleep(0.5)
        return

    def read_particules(self):
        if self.Fan==False:
            startFan()
        data = uart.read(32)
        if data is not None:
            print(data)
            if self.verify(data):
                pm10 = round(data[8] * 256 + data[9], 1)
                pm25 = round(data[6] * 256 + data[7], 1)
                return pm10,pm25
            else:
                return 0,0
        else:
            return 0,0

    def verify(self,recv):
            """
                Uses the last 2 bytes of the data packet from the Honeywell sensor
                to verify that the data recived is correct
            """
            calc = 0
            ord_arr = []
            for c in bytearray(recv[:-2]): #Add all the bytes together except the checksum bytes
                calc += c
                ord_arr.append(c)
            #self.logger.debug(str(ord_arr))
            sent = (recv[-2] << 8) | recv[-1] # Combine the 2 bytes together
            if sent != calc:
                print("Checksum failure",sent,"!=", calc)
                return False
            else:
                print("Checksum ok",sent,"==", calc)
                return True
