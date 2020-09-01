def saveFileMsgs(neighbours,counter,rtc):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) counter(int) table([id][tx_power])
        Example: 15/10/2019 13:21:31 5 id2 min_pow, id3 max_pow
        '''
        f = open('neighbour_first.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} counter {}".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter))
        for i in range(len(neighbours[0])):
            f.write(" id {} pow {}, ".format(neighbours[0][i],neighbours[1][i]))
        f.write("\n")
        f.close()
        return

def get_first_token():
    """
    It starts from the middle and goes to the first position
    """
    token=node_list[int(len(node_list))-1]
    # if len(node_list)%2==0:
    #     token=node_list[int(len(node_list)/2)-1]
    # else:
    #     token=node_list[round(len(node_list)/2)-1]
    return token
def get_next_token(token):
    """
    Decide which node will send the sensor info to the gateway
    It starts from the middle and goes down
    """
    if (node_list.index(token)-1)>0:
        token=node_list[node_list.index(token)-1]
    else:
        token=get_first_token()
    return token

def get_neighbour_power(pos):
    if len(neighbours)>0 and node_list[pos] in neighbours[0]:
        power=neighbours[1][neighbours[0].index(node_list[pos])]
        return power
    else:
        return 14

def isMyTurn(token):
    return node_list.index(id)==token

def isMyACK(token):
    return node_list.index(id)<token

def discover(id):
    #print("Discovering")
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} Start discover\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()
    power=2 #min
    com.change_txpower(power)
    global Hello_received,msg,counter
    global neighbours, End_discover
    while ((len(neighbours[0])<3) & (power<14)): #Potencia max =14
        #print("I'm in")
        #Enviar missatge inici de descoberta
        msg_tx='Discover normal %i %s'%(power,id)
        for i in range(4):
            msg=msg_aux
            com.sendData(str(msg_tx))
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} sending {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg_tx))
            f.close()
            counter=counter+1
            time.sleep(2.5+ machine.rng()%1)
            #print("he enviat",str(msg_tx))
            if "Hello" in msg:
                splitmsg=msg.split( )
                id_n=splitmsg[2]
                pow=int(splitmsg[1])
                print("Update neighbours")
                neighbours=com.update_neighbours(pow,id_n,neighbours)
                f = open('msgReceived_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} update neighbour, msg received: {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg))
                f.close()
                Hello_received=False
        #change power
        power=power+1
        com.change_txpower(power)
    #Change tx_power to the nearest neighbour
    power=neighbours[1][node_list.index(id)-1]
    #Send msg of "End discover"
    msg_retry='Discover end %i %s'%(power,node_list.index(id)+1)

    com.change_txpower(power)
    while not End_discover:
        com.sendData(str(msg_retry))
        f = open('msg_sent_first.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} sending {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg_retry))
        f.close()
        counter=counter+1
        time.sleep(2)
        print(msg_retry)

    End_discover=False
    neighbours=com.neighbours_min(id,neighbours,neighbours_aux)
    #print("He acabat discover",neighbours)
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} Discover finished\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()
    return

def handler_button(button):
    pycom.heartbeat(True)
    #print("The config is going to start")
    global mode
    global rcv_data
    mode=CONFIG_MODE
    rcv_data=True
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} Se ha pulsado el boton\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()
    counter=1

def interrupt(lora):
    print("Interrupcio")
    global rcv_data
    global msg, splitmsg
    global mode
    global config_start
    global node_list
    global Error, rtc,f
    global Hello_received,End_discover
    global msg_aux, splitmsg_aux
    global counter
    lora.power_mode(LoRa.ALWAYS_ON)

    msg_aux=com.reciveData(f,rtc)
    if msg_aux!="error":

        #saveFileMsgsReceived(msg_aux,rtc)

        if "Alarm" in msg_aux:
            rcv_data=True
            mode=ALARM_MODE
            timer_to_send_alarm.start()
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} start alarm\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
            f.close()
            return

        if (mode==CONFIG_MODE or mode==LISTEN_MODE) and ("stop" in msg_aux): #Config has finished
            msg=msg_aux
            rcv_data=False
            config_start=False
            if type(msg)==bytes:
                msg=bytes.decode(msg)
            splitmsg=msg.split()
            node_list=splitmsg[2:-1]
            f = open('neighbour_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} node_list {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],node_list))
            f.close()
            if node_list.index(id)+1==int(splitmsg[-1]):
                mode=LISTEN_MODE
                power=14
                com.change_txpower(power)
                splitmsg[-1]=str(node_list.index(id))
                msg=" ".join(splitmsg)
                com.sendData(str(msg))
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} sending {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg))
                f.close()
                print("he enviat stop")

        elif mode==LISTEN_MODE:
            #msg=msg_aux
            rcv_data=True
        if "Config" in msg_aux: #Starting config
            rcv_data=True
            mode=CONFIG_MODE
            msg=msg_aux

        if mode==NORMAL_MODE and ("Info" in msg_aux or "Token" in msg_aux):
            #msg=msg_aux
            rcv_data=True
            if type(msg_aux)==bytes:
                msg_aux=bytes.decode(msg_aux)
            splitmsg_aux=msg_aux.split()
            if "Info" in msg_aux and splitmsg_aux[2]==id:
                timer_to_send_GTW.reset()

        if mode==DISCOVER_MODE:
            try:
                if type(msg_aux)==bytes:
                    msg_aux=bytes.decode(msg_aux)
                if "Hello" in msg_aux:
                    Hello_received=True
                if "Discover normal" in msg_aux:
                    msg=msg_aux
                if "Discover end" in msg_aux and isMyACK(int(msg_aux[-1])):
                    End_discover=True
                    msg=msg_aux
                    timer_discover_end.reset()
                    mode=NORMAL_MODE
                    f = open('msg_sent_first.txt', 'a')
                    f.write("{}/{}/{} {}:{}:{} ACK discover received\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
                    f.close()
                error=False
            except Exception as e:
                 print(e)
                 error=True
    else:
        print("Receiving error")


###############################################################################
                                   #MAIN
###############################################################################

reset_cause=machine.reset_cause()
button.callback(trigger=Pin.IRQ_FALLING, handler=handler_button)

if reset_cause==machine.DEEPSLEEP_RESET:
    com=comu.Comunication()
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} Start Join\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()
    #com.Switch_to_LoraWan()
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} Finish Join\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()

    if com.lora.has_joined()==False:
         com.JoinLoraWan()
         time.sleep(2)
    com.Switch_to_LoraRaw()
    com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
    counter=pycom.nvs_get("count")
    node_list=[]
    neighbours=[[],[]]
    mode=CONFIG_MODE #NORMAL_MODE
    msg="Config 2"
    rcv_data=True
    print("Good morning!")

else:
    rcv_data=True
    com=comu.Comunication()
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} start Join\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()
    #com.JoinLoraWan()
    #com.Switch_to_LoraRaw()
    f = open('msg_sent_first.txt', 'a')
    f.write("{}/{}/{} {}:{}:{} finish Join\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
    f.close()
    time.sleep(2)

    com.start_LoraRaw()
    com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
    print("All OK, please press the button")

while rtc.now()[3]<hora+5:
    if mode==ALARM_MODE:
        if timer_to_send_alarm.read()>=120: #2min
            #com.Switch_to_LoraWan()
            print("Sending to GTW")
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} Sending to gateway\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
            f.close()
            #com.EnviarGateway(com.ApplyFormat(msg_alarm.split( )))
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} Alarm sent\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
            f.close()
            timer_to_send_alarm.reset()
            timer_to_send_alarm.start()
            #com.Switch_to_LoraRaw()
        if rcv_data:
            rcv_data=False
            msg_alarm=msg_aux[:]
            #splitmsg=msg_aux.split( )
            if "Alarm" in msg_aux and "ok" not in msg_aux :
                splitmsg_alarm=msg_alarm.split( )
                msg_alarm_ok="Alarm ok "+str(id)+" "+str(splitmsg_alarm[1])   #Alarm ok from:id to:id
                com.sendData(msg_alarm_ok)
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} sending {} \n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg_alarm_ok))
                f.close()

            if "Alarm ok" in msg_aux:
                mode=NORMAL_MODE
                token=get_first_token()
                com.change_txpower(get_neighbour_power(node_list.index(token)))
                #After alarm ok, start again the proocess
                intent=1
                mode=CONFIG_MODE
                rcv_data=True
                EnviatGateway=False
                neighbours=[[],[]]
                neighbours_aux=[[],[]]
                msg="Config 2"
                msg_aux="Config 2"
                rcv_data=False
                node_list=""
                msg_alarm_ok=" "
                Hello_received=False
                period=2
                counter=1
                i=0
                timer_to_send_GTW.reset()
                timer_to_send_GTW.start()
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} stop alarm\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
                f.close()
                time.sleep(60) #1min




                # msg_send="Token"+" "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)+1])
                # com.sendData(msg_send)
                # token_ack=False
                # print("Sending token: ",msg_send)
                # timer_token_ack.reset()
                # timer_to_send_alarm.reset()
                # timer_token_ack.start()
                # timer_to_send_alarm.stop()
                #intent=1
        else:
            print("Sending ",msg_alarm_ok)
            com.sendData(msg_alarm_ok)
            time.sleep(2)

    if mode==CHECK:
        com.sendData("Hay buena cobertura con ramon llull "+str(i))
        com.change_txpower(14)
        i=i+1
        if i>50:
            i=0
        time.sleep(4)
    if mode==CONFIG_MODE:
        if rcv_data:
            config_start=True
            #print("He rebut: ",msg)
            print("Part 1 ",id not in msg)
            if id not in msg:
                rcv_data=False
                splitmsg=msg.split( )
                id_n=splitmsg[-1]
                pow=int(splitmsg[1])
                com.change_txpower(pow)
                com.sendData(msg+" "+str(id))
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} config start, sending {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter,msg+" "+str(id)))
                f.close()
                counter=counter+1
                print("Enviare: ",msg+" "+str(id))
                #update_neighbours(pow,id_n)

        print("Part 2 ",msg,rcv_data,id in msg)
        if (rcv_data==True) and (id in msg) and (config_ACK==False):
            rcv_data=False
            if "Config" in msg:
                config_ACK=True
                print("He rebut ACK")
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} ack config, msg received {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg))
                f.close()
                splitmsg=msg.split( )
                id_n=splitmsg[-1]
                pow=int(splitmsg[1])
                #update_neighbours(pow,id_n)
                mode=LISTEN_MODE

        print("Part 3 ",config_ACK, config_start)
        if config_ACK==False and config_start==True:
            if intent<3:
                com.sendData(msg+" "+str(id))
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} intent config {}, msg sent: {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter,msg+" "+str(id)))
                f.close()
                counter=counter+1
                time.sleep(2+machine.rng()%1)
                print("Enviare %s intent: "%(intent),msg+" "+str(id))
                intent=intent+1
            elif power<14: #Max power=14
                intent=1
                power=power+1
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                splitmsg=msg.split( )
                splitmsg[1]=str(power)
                msg=" ".join(splitmsg)
                com.change_txpower(power)
            else:
                power=2
                intent=1
                com.change_txpower(power)

    if mode==LISTEN_MODE:

        if (rcv_data==True):
            msg=msg_aux

            if type(msg_aux)==bytes:
                msg=bytes.decode(msg_aux)
            splitmsg=msg.split()

            rcv_data=False
            missatge=True

            if "Discover normal" in msg and missatge==True:
                missatge=False
                id_n=splitmsg[-1]
                pow=int(splitmsg[2])
                com.change_txpower(pow)
                print("Enviare", "Hello ",pow , " ", id )
                time.sleep(machine.rng()%2)
                com.sendData("Hello "+ str(pow) + " "+ str(id))
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} sending {}  counter {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],"Hello "+ str(pow) + " "+ str(id),counter))
                f.close()
                counter=counter+1
                neighbours_aux=com.update_neighbours(pow,id_n,neighbours_aux)
                rcv_data=False
            elif "Discover next" in msg:
                if isMyTurn(int(msg[-1]))==True:
                    mode=DISCOVER_MODE

    elif mode==DISCOVER_MODE:
        f = open('msg_sent_first.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} start discover\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
        f.close()
        discover(id)
        f = open('msg_sent_first.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} finish discover\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
        f.close()
        print("He acabat discover", neighbours)
        saveFileMsgs(neighbours,counter,rtc)
        timer_discover_end.start()
        timer_discover_end.reset()
        while (timer_discover_end.read()<4):
            time.sleep(2)
        timer_discover_end.stop()
        #Init normal_mode
        mode=NORMAL_MODE
        rcv_data=False
        token=get_first_token()
        com.change_txpower(get_neighbour_power(node_list.index(token)))
        msg_send="Token"+" "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)+1])
        com.sendData(msg_send)
        token_ack=False
        print("Sending token: ",msg_send)
        f = open('msg_sent_first.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} sending {} \n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg_send))
        f.close()
        timer_token_ack.reset()
        timer_token_ack.start()
        intent=1

        # print("Enviar a gateway")
        # com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=None)
        # com.Switch_to_LoraWan()
        # msg=com.ApplyFormat_NeighboursTable(neighbours,counter)
        # com.EnviarGateway(msg)
        # # com.Switch_to_LoraRaw()
        # # com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
        # # print("LoraRaw Ok")
        # EnviatGateway=True
        # com.lora.nvram_save()
        # saveFileMsgs(neighbours,counter,rtc)
        # counter=counter+1
        # pycom.nvs_set("count",counter)
        # print("DeepSleep ",counter)
        # machine.deepsleep((period*60*1000)+300) #5.3min, machine.deepsleep([time_ms])


    elif mode==NORMAL_MODE:
        if rcv_data==True:
            msg=msg_aux
            splitmsg=msg.split( )
            rcv_data=False
            print("Check info ok ", splitmsg[2]==id)
            if "Info" in msg and splitmsg[1]==token:
                com.change_txpower(14) #This msg's important, so it's send to the max_power
                com.sendData("Info ok "+str(id))
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} sending info ok\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
                f.close()

                print("he enviat info ok",msg)
                data=com.ApplyFormat(splitmsg)
                #token=splitmsg[1]
                token_ack=True
                print(data)
                timer_to_send_GTW.reset()
                timer_to_send_GTW.start()
                intent=1
            elif "Token" in msg and (splitmsg[2]==token):
                token_ack=True
                EnviatGateway=False
                timer_token_ack.reset()
                timer_token_ack.stop()
                intent=1


        if timer_to_send_GTW.read()>=120: #4.10 min=250
            print("Enviar a gateway")
            timer_to_send_GTW.reset()
            #timer_to_send_GTW.stop()
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} Start sending to gateway data {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],data))
            f.close()
            #com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=None)
            #com.Switch_to_LoraWan()
            #com.EnviarGateway(data)
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} Finish sending to gateway data {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],data))
            f.close()
            #com.Switch_to_LoraRaw()
            com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
            print("LoraRaw Ok")
            EnviatGateway=True
            token=get_next_token(token)
            timer_token_ack.reset()
            timer_token_ack.start()
            msg_send="Token"+" "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(token)])
            token_ack=False
            intent=1
            if token==get_first_token():
                #End_normal=True
                print("Finished")
                f = open('msg_sent_first.txt', 'a')
                f.write("Sudidos los mensajes de info de todos los nodos\n")
                f.close()
                #save_parameters()
                #com.Switch_to_LoraWan()
                #com.savestate()
                #mode=CONFIG_MODE
                #machine.deepsleep(500)

        if timer_token_ack.read()>=60 and token_ack==False:
            com.sendData(msg_send)
            f = open('msg_sent_first.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} counter {} token_ack {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter,msg_send))
            f.close()
            counter=counter+1
            print("Sending token: ",msg_send)
            timer_token_ack.reset()
            intent=intent+1
            if intent==10:
                print("he fet més de 10 intents")
                token=get_next_token(token)
                com.change_txpower(get_neighbour_power(node_list.index(token)))
                msg_send="Token"+" "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(token)])
                f = open('msg_sent_first.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} more than 10 intents change token to: {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],msg_send))
                f.close()
                intent=1
