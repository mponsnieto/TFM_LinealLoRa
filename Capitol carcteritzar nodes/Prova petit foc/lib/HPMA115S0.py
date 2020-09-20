from machine import UART
import time

# this uses the UART_1 default pins for TXD and RXD (``P3`` and ``P4``)
uart = UART(1, baudrate=9600)

class HPMA1150S0:
    def __init__(self):
        self.Fan=True
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

    def read_particules(self,rtc):
        # if self.Fan==False:
        #     startFan()
        data = uart.read(32)
        if data is not None:
            print(data)
            if data[0]==66 and data[1]==77:
                pm1 = round(data[4] * 256 + data[5], 1)
                pm25 = round(data[6] * 256 + data[7], 1)
                pm10 = round(data[8] * 256 + data[9], 1)
                f = open('data_QAire.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} {} {} {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],pm1,pm25,pm10))
                f.close()
                return pm1,pm25,pm10
            else:
                return -1,-1,-1
        else:
            return 0,0,0

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
