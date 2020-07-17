from network import LoRa
import socket
import ubinascii
import struct
import time
from machine import Pin, I2C
import pycom
import ustruct
from ustruct import unpack as unp
import math
from crypto import AES
import crypto
import binascii

class Comunication:
    def __init__(self):
        self.key = b'encriptaincendis'
        pass
    # Initialize LoRa in LORAWAN mode.
    def JoinLoraWan(self):
        self.lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)

        # create an OTA authentication params
        app_eui = ubinascii.unhexlify('70B3D57ED001C55E')
        dev_eui = ubinascii.unhexlify('006D2D7767E7BAFE') # these settings can be found from TTN
        #app_eui = ubinascii.unhexlify('70B3D57ED0019255') # these settings can be found from TTN
        app_key = ubinascii.unhexlify('0A05862CEA15FC56C047FC03FBDF34DB') # these settings can be found from TTN

        # set the 3 default channels to the same frequency (must be before sending the OTAA join request)
        self.lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
        self.lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
        self.lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

        # join a network using OTAA
        self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        while not self.lora.has_joined():
            time.sleep(2.5)
            print('Not joined yet...')

        # remove all the non-default channels
        for i in range(3, 16):
            self.lora.remove_channel(i)

        # create a LoRa socket
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # make the socket non-blocking
        self.s.setblocking(False)

        time.sleep(5)

    """ Your own code can be written below! """

    def start_LoraRaw(self):
        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setblocking(False)#Aquesta instrucció igual sobra
        time.sleep(5)
        lora=self.lora
        #return(lora)

    def change_txpower(self,power):
        self.lora.tx_power(power)

    def savestate(self):
        self.lora.nvram_save()

    def Switch_to_LoraRaw(self):
        self.lora.nvram_save()
        self.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setblocking(False)#Aquesta instrucció igual sobra
        time.sleep(5)

    def Switch_to_LoraWan(self):
        self.lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)
        self.lora.nvram_restore()
        time.sleep(5)
        #Si no es reinicia el socket el missatge 3 no s'envia
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    def EnviarGateway(self,data):
        self.s.send(data)
        time.sleep(5)

    def sendData(self,msg,rtc,f):
        f=open('msg_sent_middle1.txt','a')
        f.write("{}/{}/{} {}:{}:{} msg {} stats {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg,self.lora.stats()))
        f.close()
        self.s.setblocking(True)
        iv = crypto.getrandbits(128) # hardware generated random IV (never reuse it)
        cipher = AES(self.key, AES.MODE_CFB, iv)
        misg_crc=misg+" "+str(self.calculate_crc(msg))
        msg = iv + cipher.encrypt(misg_crc)
        self.s.send(msg)
        self.s.setblocking(False)
        #print(msg)
        #print(len(msg))
        #time.sleep(5)

    def reciveData(self,rtc,f):
        self.s.setblocking(False)
        msg=self.s.recv(128)#Get any data recieved
        #If there's any data, decrypt
        if (len(msg)>0):
            try:
                #print("encriptat: ",msg)
                cipher = AES(self.key, AES.MODE_CFB, msg[:16]) # on the decryption side
                original = cipher.decrypt(msg[16:])
                print("original ",original)
                if "Config" in original or "stop" in original or "Discover" in original or "Hello" in original or "Info" in original or "Token" in original or "Alarm" in original or "Hay" in original:
                    crc_OK,msg=self.check_crc(original)
                    if crc_OK:
                        f=open('msg_received_middle2.txt','a')
                        f.write("{}/{}/{} {}:{}:{} msg {} stats {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg,self.lora.stats()))
                        f.close()
                        return(msg)
                    else:
                        print("CRC not OK")
                        return("error")
                else:
                    return("error")
            except Exception as e:
                print(e)
                return("error")
        else:
            return("error")

    def update_neighbours(self,pow,id_n,neighbours):
        if id_n in neighbours[0]:
            if pow < neighbours[1][neighbours[0].index(id_n)]:
                neighbours[1][neighbours[0].index(id_n)]=pow
        else:
            neighbours[0].append(id_n)
            neighbours[1].append(pow)
            #print("I have a friend ")
        print(neighbours)
        return neighbours

    def neighbours_min(self,neighbours,neighbours_aux):
        for id in neighbours[0]:
            if id in neighbours_aux[0]:
                neighbours[1][neighbours[0].index(id)]=min(neighbours[1][neighbours[0].index(id)],neighbours_aux[1][neighbours_aux[0].index(id)])
        print(neighbours)
        return(neighbours)


    def ApplyFormat(self,splitmsg):
        packet_dust= ustruct.pack('f',int(splitmsg[3]))
        packet_tempC= ustruct.pack('f',int(splitmsg[4]))
        packet_Tht= ustruct.pack('f',int(splitmsg[5]))
        packet_Hht= ustruct.pack('H',round(int(splitmsg[6])*100))
        packet_tbmp= ustruct.pack('f',int(splitmsg[7]))
        packet_val= ustruct.pack('H',int(splitmsg[8]))
        packet_dhi= ustruct.pack('b',int(splitmsg[9]))
        #+packet_TCam=ustruct.pack('f',int(splitmsg[10]))
        return(packet_dust+packet_tempC+packet_Tht+packet_Hht+packet_tbmp+packet_val+packet_dhi)#+packet_TCam)

    def calculate_crc(self,msg):
        """
        Compute CRC
        """
        if type(msg)==bytes:
            msg=bytes.decode(msg)
        crc = 0
        data=bin(int(binascii.hexlify(msg),16))
        data=str.encode(data)
        for i in range(len(data)):
            byte = data[i]
            for b in range(8):
                fb_bit = (crc ^ byte) & 0x01
                if fb_bit == 0x01:
                    crc = crc ^ 0x18
                crc = (crc >> 1) & 0x7f
                if fb_bit == 0x01:
                    crc = crc | 0x80
                byte = byte >> 1
        return crc

    def check_crc(self,msg):
            """
            Check if CRC received is correct
            """
            if type(msg)==bytes:
                msg=bytes.decode(msg)
            splitmsg=msg.split( )
            crc_rcv=int(splitmsg[-1])
            aux=" ".join(splitmsg[:-1]) #Not including the CRC received
            crc_new = self.calculate_crc(aux)
            return (crc_new==crc_rcv,aux)
