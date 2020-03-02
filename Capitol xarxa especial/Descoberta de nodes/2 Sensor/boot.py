import pycom
import comunication as comu
import machine
from machine import Timer
import ubinascii
from network import LoRa
import socket
import time

Hello_received=False
end_discover=False
CONFIG_MODE=0
DISCOVER_MODE=1
LISTEN_MODE=2
NORMAL_MODE=3
ALARM_MODE=4
stop_config=False
pycom.wifi_on_boot(False)
timer2=Timer.Chrono()
timer3=Timer.Chrono()
timer_Disc_end=Timer.Chrono()
timer_Disc_end.reset()
timer_read_sensors=Timer.Chrono()
timer_read_sensors.reset()
discover_end_ack=False
timer2.reset()
missatge=False
periode=500
pycom.wifi_on_boot(False)

com=comu.Comunication()
com.start_LoraRaw()
#timer=Timer.Chrono()
#timer.reset()

id=ubinascii.hexlify(machine.unique_id()).decode('utf-8')#'3c71bf8775d4'
print("id del dispositiu: ",id)
mode=CONFIG_MODE
a=False
config_ACK=False
token_ack=True
stop_ACK=False
config_start=False
power=2
rcv_data=False
stop_start=False
info_ack=True
info_passed=False
readen=False #borrar
msg=" "
msg_alarm=" "
msg_listen=" "
msg_alarm_ok=" "
neighbours=[[],[]]
neighbours_aux=[[],[]]
intent=1
