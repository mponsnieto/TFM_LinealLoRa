import pycom
import comunication as comu
import machine
import ubinascii
from network import LoRa
import socket
import time
import pycom
from machine import Pin, I2C
from ustruct import unpack as unp
from machine import Timer
#Inicialitzacions llegir sensors:
#Inicialitzacions
CONFIG_MODE=0
DISCOVER_MODE=1
LISTEN_MODE=2
NORMAL_MODE=3
ALARM_MODE=4
CHECK=5
stop_config=False


id=ubinascii.hexlify(machine.unique_id()).decode('utf-8')#'3c71bf8775d4'
print("id del dispositiu: ",id)
mode=CHECK
config_ACK=False
config_start=True
power=2
rcv_data=False
intent=1
node_list=[]
neighbours=[[],[]]
neighbours_aux=[[],[]]
msg="Config 2"
node_list=""
msg_alarm_ok=" "
error=False
Hello_received=False
End_discover=False
info_passed=False
timer=Timer.Chrono()

period=2

pycom.wifi_on_boot(False)

counter=1
i=0
## Initialize time
rtc = machine.RTC()
#(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
rtc.init((2020, 07, 15, 0,0))
