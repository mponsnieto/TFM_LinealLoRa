import comunication as comu
import machine
from machine import Timer
from machine import Pin
import ubinascii
from network import LoRa
import socket
import time
import pycom

CONFIG_MODE=0
DISCOVER_MODE=1
LISTEN_MODE=2
NORMAL_MODE=3
ALARM_MODE=4
pycom.wifi_on_boot(False)

com=comu.Comunication()
com.JoinLoraWan()
time.sleep(2)
com.Switch_to_LoraRaw()
com.start_LoraRaw()

id=ubinascii.hexlify(machine.unique_id()).decode('utf-8')#'3c71bf8775d4'
print("id del dispositiu: ",id)
mode=LISTEN_MODE #CONFIG_MODE #LISTEN_MODE
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
node_list=""
msg_alarm_ok=" "
timer_to_send_GTW=Timer.Chrono()
timer_to_send_alarm=Timer.Chrono()
timer_token_ack=Timer.Chrono()
timer_discover_end=Timer.Chrono()
button = machine.Pin(Pin.exp_board.G17, mode=Pin.IN, pull=Pin.PULL_UP)

Hello_received=False

## Initialize time
rtc = machine.RTC()
#(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
rtc.init((2019, 11, 27, 15,26))
