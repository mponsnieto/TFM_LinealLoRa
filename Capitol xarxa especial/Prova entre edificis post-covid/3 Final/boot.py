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
timer2=Timer.Chrono()
timer3=Timer.Chrono()
timer_read_sensors=Timer.Chrono()
timer_Disc_end=Timer.Chrono()
timer_Disc_end.reset()
timer.reset()
timer2.reset()
discover_end_ack=False

period=2

pycom.wifi_on_boot(False)

counter=1
i=0
## Initialize time
rtc = machine.RTC()
#(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
f = open('process_final.txt', 'a')
f.write("{}/{}/{} {}:{}:{} Nodo sensor en marcha\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
f.close()
f=open('msg_received_final.txt','a')
f.write("------------------------\n")
f.close()
f=open('msg_sent_final.txt','a')
f.write("------------------------\n")
f.close()
f=open('neighbours_sent_final.txt','a')
f.write("------------------------\n")
f.close()
