from machine import Pin
import machine
import pycom
# initialize GP17 in gpio mode and make it an input with the
# pull-up enabled

def handler_button(button):
    #get value, 0 or 1
    print(p_in.value())


button = machine.Pin(Pin.exp_board.G17, mode=Pin.IN, pull=Pin.PULL_UP)
button.callback(trigger=Pin.IRQ_FALLING, handler=handler_button)
while True:
    pass
