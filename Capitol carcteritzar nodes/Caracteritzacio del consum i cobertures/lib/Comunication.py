from network import LoRa
import socket
import ubinascii
import struct
import time
from machine import Pin, I2C
import pycom
from ustruct import unpack as unp
import math
from crypto import AES
import crypto

app_eui_radial='70B3D57ED001C55E'
app_eui_lineal='70B3D57ED001C55A'
dev_eui_R_Caterina='006D2D7767E7BAFE'
dev_eui_R_Marta='0058A97F44896904'
app_key_R_Caterina='0A05862CEA15FC56C047FC03FBDF34DB'
app_key_R_Marta='AEAFACB81C594C7B7BE3466241CD38EF'

class Comunication:
    def __init__(self):
        self.key = b'encriptaincendis'
        pass
    # Initialize LoRa in LORAWAN mode.
    def JoinLoraWan(self):
        self.lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)

        # create an OTA authentication params
        app_eui = ubinascii.unhexlify('70B3D57ED001C55E')
        dev_eui = ubinascii.unhexlify('0058A97F44896904') # these settings can be found from TTN
        #app_eui = ubinascii.unhexlify('70B3D57ED0019255') # these settings can be found from TTN
        app_key = ubinascii.unhexlify('AEAFACB81C594C7B7BE3466241CD38EF') # these settings can be found from TTN

        # set the 3 default channels to the same frequency (must be before sending the OTAA join request)
        self.lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
        self.lora.add_channel(1, frequency=868100000, dr_min=0, dr_max=5)
        self.lora.add_channel(2, frequency=868100000, dr_min=0, dr_max=5)

        # join a network using OTAA
        self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        while not self.lora.has_joined():
            time.sleep(5)
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

    def savestate(self):
        self.lora.nvram_save()

        # def restorestate(self):
        #     self.lora.nvram_restore()

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

    def RebreGateway(self):
        data,port = self.s.recvfrom(256)
        print(data)

    def sendData(self,misg):
        self.s.setblocking(True)
        iv = crypto.getrandbits(128) # hardware generated random IV (never reuse it)
        cipher = AES(self.key, AES.MODE_CFB, iv)
        msg = iv + cipher.encrypt(misg)
        self.s.send(msg)
        self.s.setblocking(False)
        #print(msg)
        #print(len(msg))
        time.sleep(5)

    def reciveData(self):
        self.s.setblocking(False)
        msg=self.s.recv(128)#Get any data recieved
        #If there's any data, decrypt
        if len(msg)>0:
            print("encriptat: ",msg)
            cipher = AES(self.key, AES.MODE_CFB, msg[:16]) # on the decryption side
            original = cipher.decrypt(msg[16:])
            print("original ",original)
            return(original)
        else:
            return
