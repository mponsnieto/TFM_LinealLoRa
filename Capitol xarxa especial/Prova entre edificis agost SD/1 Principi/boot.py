import comunication as comu
import machine
from machine import Timer
from machine import Pin, SD
import ubinascii
from network import LoRa
import socket
import time
import pycom
import os

sd = SD()
os.mount(sd, '/sd')

# check the content
os.listdir('/sd')

CONFIG_MODE=0
DISCOVER_MODE=1
LISTEN_MODE=2
NORMAL_MODE=3
ALARM_MODE=4
CHECK=5
pycom.wifi_on_boot(False)
pycom.heartbeat(False)


id=ubinascii.hexlify(machine.unique_id()).decode('utf-8')#'3c71bf8775d4'
print("id del dispositiu: ",id)
mode=CHECK#LISTEN_MODE #CONFIG_MODE #LISTEN_MODE
config_ACK=False
token_ack=False
config_start=False
End_discover=False
End_normal=False
power=2
intent=1

EnviatGateway=False
neighbours=[[],[]]
neighbours_aux=[[],[]]
msg="Config 2"
msg_aux="Config 2"
rcv_data=False
node_list=""
msg_alarm_ok=" "

timer_to_send_GTW=Timer.Chrono()
timer_to_send_alarm=Timer.Chrono()
timer_token_ack=Timer.Chrono()
timer_discover_end=Timer.Chrono()
button = machine.Pin(Pin.exp_board.G17, mode=Pin.IN, pull=Pin.PULL_UP)
#timer_to_send_GTW.start()
Hello_received=False

period=2

counter=1
i=0
## Initialize time
rtc = machine.RTC()
#(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
hora=00
rtc.init((2020, 09, 09, hora,00))
f = open('/sd/msg_sent_first.txt', 'a')
f.write("------------------------\n")
f.close()
f = open('/sd/msgReceived_first.txt', 'a')
f.write("------------------------\n")
f.close()
f = open('/sd/neighbour_first.txt', 'a')
f.write("------------------------\n")
f.close()
f = open('/sd/msg_sent_first.txt', 'a')
f.write("{}/{}/{} {}:{}:{} LoPy ON id {} \n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],id))
f.close()
