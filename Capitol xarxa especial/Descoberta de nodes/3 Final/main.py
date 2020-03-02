
def save_parameters():
    """
    Save parameters to nv_ram before the deepsleep
    """
    global node_list,neighbours
    for l in range(len(node_list)):
        print(l)
        name="node"+str(l)
        print(name,node_list[l])
        pycom.nvs_set(name,node_list[l])
        leng=l
    pycom.nvs_set("len_node",leng+1)
    for l in range(len(neighbours[1])):
        name="neighbour"+str(l)
        name2="power"+str(l)
        pycom.nvs_set(name,neighbours[0][l])
        pycom.nvs_set(name2,neighbours[1][l])
        leng=l
    pycom.nvs_set("len_neighbours",leng+1)
    com.savestate()
    return

def get_neighbour_power(pos):
    """
    Get the tx power of a certain neighbour
    """
    if len(neighbours)>0 and (node_list[pos] in neighbours):
        power=neighbours[1][neighbours[0].index(node_list[pos])]
        return power
    else: #If the power isn't saved during the DISCOVER, return max power
        return 12

def get_first_token():
    """
    It starts from the middle and goes to the first position
    """
    if len(node_list)%2==0:
        token=node_list[int(len(node_list)/2)]
    else:
        token=node_list[round(len(node_list)/2)]
    return token
def get_next_token(token):
    """
    Decide which node will send the sensor info to the gateway
    It starts from the middle and goes down
    """
    if (node_list.index(token)+1)<node_list.index(id):
        token=node_list[node_list.index(token)+1]
    else:
        token=get_first_token()
    return token

def discover(id):
    global Hello_received,End_discover
    global neighbours
    print("Discovering")
    power=2 #min
    com.change_txpower(power)

    while ((len(neighbours[0])<3) & (power<14)): #Potencia max =14
        print("I'm in")
        #Enviar missatge inici de descoberta
        msg_tx='Discover normal %i %s'%(power,str(id))
        for i in range(4):
            msg=aux
            com.sendData(str(msg_tx))
            time.sleep(2.5+ machine.rng()%1)
            print(msg_tx)
            if "Hello" in msg:
                splitmsg=msg.split( )
                print("Update neighbour ",msg)
                id_n=splitmsg[2]
                pow=int(splitmsg[1])
                #print("Update neighbours")
                neighbours=com.update_neighbours(pow,id_n,neighbours)
                Hello_received=False
                msg=aux
        #change power
        power=power+1
        com.change_txpower(power)

    #Send msg of "End discover"
    #Change tx_power to the nearest neighbour
    power=get_neighbour_power(node_list.index(id)-1)
    msg_retry='Discover next %i %s'%(power,node_list.index(id)-1)
    com.change_txpower(power)
    while not End_discover:
        com.sendData(str(msg_retry))
        time.sleep(5)
        print(msg_retry)

    End_discover=False
    print("He acabat discover",neighbours)
    return

def interrupt(lora):
    print("Interrupcio")
    global rcv_data
    global msg, aux, error
    global mode
    global Hello_received, End_discover, stop_config

    aux=com.reciveData()
    if aux!="error":
        if "Alarm" in aux:
            rcv_data=True
            mode=ALARM_MODE
            timer_to_send_alarm.start()
            return

        if mode==LISTEN_MODE:
            rcv_data=True
            msg=aux
        if mode==DISCOVER_MODE:
            try:
                if type(aux)==bytes:
                    aux=bytes.decode(aux)
                if "Hello" in aux:
                    Hello_received=True

                if "Discover normal" in aux:
                    End_discover=True
                    msg=aux
                error=False
            except Exception as e:
                 print(e)
                 error=True
        if mode==CONFIG_MODE and ("stop" in aux): #Config has finished
            stop_config=True
            rcv_data=True
            msg=aux
            splitmsg=msg.split( )

        if "Config" in aux and (stop_config==False): #Starting config
            rcv_data=True
            mode=CONFIG_MODE
            msg=aux
        if mode==NORMAL_MODE and ("Info" in aux or "Token" in aux):
            #msg=msg_aux
            rcv_data=True
            if type(aux)==bytes:
                aux=bytes.decode(aux)
            splitmsg_aux=aux.split()
            if "Info" in aux and splitmsg_aux[2]==id:
                timer_to_send_GTW.reset()
    else:
        print("Receiving error")

def isMyTurn(token):
    #The token is for me
    return node_list.index(id)==token
def isMyACK(token):
    return node_list.index(id)<token

###############################################################################
                                   #MAIN
###############################################################################

com=comu.Comunication()
reset_cause=machine.reset_cause()
if reset_cause==machine.DEEPSLEEP_RESET:
    com.lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)
    com.lora.nvram_restore()
    if com.lora.has_joined()==False:
        com.JoinLoraWan()
    # com.JoinLoraWan()
    time.sleep(2)
    com.Switch_to_LoraRaw()
    # com.start_LoraRaw()
    len_node=pycom.nvs_get("len_node")
    len_neighbours=pycom.nvs_get("len_neighbours")
    node_list=[]
    neighbours=[[],[]]
    for l in range(len_node):
        name="node"+str(l)
        node=pycom.nvs_get(name)
        node_list.append(node)
    for l in range(len_neighbours):
        name="neighbour"+str(l)
        name2="power"+str(l)
        ids=pycom.nvs_get(name)
        powers=pycom.nvs_get(name2)
        neighbours[0].append(ids)
        neighbours[1].append(powers)
    mode=NORMAL_MODE
    #Prepare the normal mode start
    token=get_first_token()
    com.change_txpower(get_neighbour_power(node_list.index(id)-1))
    msg_send="Token "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)-1])
    com.sendData(msg_send)
    token_ack=False
    timer_token_ack.start()
    intent=1
    print("Good morning!")

else:
    com.JoinLoraWan()
    time.sleep(2)
    com.Switch_to_LoraRaw()
    com.start_LoraRaw()

com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
com.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868,tx_power=power)

while True:
    if mode==ALARM_MODE:
        if rcv_data:
            print("Alarm")
            rcv_data=False
            msg_alarm=aux[:]
            if "Alarm" in aux and "ok" not in aux:
                splitmsg_alarm=msg_alarm.split( )
                msg_alarm_ok="Alarm ok "+str(id)+" "+str(splitmsg_alarm[1]) #Alarm ok from:id to:id
                com.sendData(msg_alarm_ok)
                #if timer_to_send_alarm.read()>=30:
                com.Switch_to_LoraWan()
                print("Sending alarm to GTW")
                com.EnviarGateway(com.ApplyFormat(msg_alarm.split( )))
                timer_to_send_alarm.reset()
                timer_to_send_alarm.start()
                com.Switch_to_LoraRaw()
            if "Alarm ok" in aux:
                mode=NORMAL_MODE
                token=get_first_token()
                com.change_txpower(get_neighbour_power(node_list.index(id)-1))
                msg_send="Token"+" "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)-1])
                com.sendData(msg_send)
                token_ack=False
                print("Sending token: ",msg_send)
                timer_token_ack.reset()
                timer_token_ack.start()
                intent=1
        else:
            print("Sending: ",msg_alarm_ok)
            com.sendData(msg_alarm_ok)
            time.sleep(2)

    if mode==CONFIG_MODE:
        if rcv_data and error==False:
            print("Part 1 ",id not in msg, config_start)
            if id not in msg and config_start==True:
                rcv_data=False
                splitmsg=msg.split( )
                id_n=splitmsg[-1]
                power=int(splitmsg[1])
                print("power1:",power)
                com.change_txpower(power)
                com.sendData(msg+" "+str(id))
                print("Enviare: ",msg+" "+str(id))
                config_start=False
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                if node_list=="":
                    splitmsg=msg.split( )
                    node_list=splitmsg[2:]
                    com.get_node_list(node_list)
                timer.start()
                while timer.read()<6:
                    if rcv_data==True and id not in msg:
                        if type(msg)==bytes:
                            msg=bytes.decode(msg)
                        splitmsg=msg.split( )
                        node_list2=splitmsg[2:]
                        if node_list2!=node_list:
                            timer.reset()

                node_list.append(str(id))
                com.get_node_list(node_list)
                msg=" ".join(splitmsg)
                msg="stop "+str(power)+" "+str(" ".join(node_list))+" "+str(node_list.index(id))
                com.sendData(msg)
                msg_retry=msg
                splitmsg=msg.split( )
                print("Enviare: ",msg)
                #time.sleep(5)

        #print("Part 2 ",msg,rcv_data,id in msg)
        if (rcv_data==True) and (id in msg) and ("stop" in msg) and int(msg.split()[-1])<node_list.index(id) and error==False:
            rcv_data=False
            config_ACK=True
            print("He rebut ACK")
            mode=DISCOVER_MODE
            config_start=False
            print("He acabat el config")


        #print("Part 3 ",config_ACK, config_start)
        if config_ACK==False and config_start==False:
            if intent<3:
                com.sendData(msg_retry)
                print("Enviare %s intent: "%(intent),msg_retry)
                #time.sleep(5)
                time.sleep(2+ machine.rng()%2.5)
                intent=intent+1
            elif power<14: #Max power=14
                intent=1
                power=power+1
                if type(msg_retry)==bytes:
                    msg_retry=bytes.decode(msg_retry)
                splitmsg=msg_retry.split( )
                splitmsg[1]=str(power)
                msg_retry=" ".join(splitmsg)
                print("power2:",power)
                com.change_txpower(power)
            else:
                power=2
                intent=1
                com.change_txpower(power)
    elif mode==DISCOVER_MODE:
        time.sleep(5)
        discover(id)
        mode=LISTEN_MODE
        print("End my discover")
    elif mode==LISTEN_MODE:
        if (rcv_data==True):
            rcv_data=False
            try:
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                splitmsg=msg.split()
            except Exception as e:
                 print(e)
                 msg="error"
            if ("Discover normal") in msg: #Other node is discovering
                id_n=splitmsg[-1]
                pow=int(splitmsg[2])
                com.change_txpower(pow)
                print("Enviare", "Hello ",pow , " ", id )
                time.sleep(machine.rng()%1)
                com.sendData("Hello "+ str(pow) + " "+ str(id))
                neighbours_aux=com.update_neighbours(pow,id_n,neighbours_aux)
            elif "Discover end" in msg and isMyTurn(int(msg[-1])): #All discovers are finished
                print("mode = normal")
                #Init normal_mode
                print("mode normal")
                mode=NORMAL_MODE
                neighbours=com.neighbours_min(neighbours,neighbours_aux,id)
                rcv_data=False
                token=get_first_token()
                com.change_txpower(get_neighbour_power(node_list.index(id)-1))
                msg_send="Token "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)-1])
                com.sendData(msg_send)
                print("He enviat token", msg)
                token_ack=False
                timer_token_ack.start()
                intent=1

    elif mode==NORMAL_MODE:
        if rcv_data==True:
            msg=aux
            rcv_data=False
            print("MODE NORMAL msg= ", msg)
            if type(msg)==bytes:
                msg=bytes.decode(msg)
            splitmsg=msg.split()
            if "Info" in msg and splitmsg[2]==id:
                com.change_txpower(14) #This msg's important, so it's send to the max_power
                com.sendData("Info ok "+str(id))
                data=com.ApplyFormat(splitmsg)
                token=splitmsg[1]
                print(data)
                timer_to_send_GTW.start()
                token_ack=True
            elif "Token" in msg and splitmsg[1]==token:
                token_ack=True
                EnviatGateway=False
                timer_token_ack.reset()
                timer_token_ack.stop()
                intent=1


        if timer_to_send_GTW.read()>=300: #5min
            com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=None)
            #time.sleep(2)
            com.Switch_to_LoraWan()
            com.EnviarGateway(data)
            print("Enviar a gateway")
            timer_to_send_GTW.reset()
            timer_to_send_GTW.stop()
            com.Switch_to_LoraRaw()
            com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
            print("LoraRaw Ok")
            EnviatGateway=True
            token=get_next_token(token)
            msg_send="Token "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)-1])
            token_ack=False
            timer_token_ack.reset()
            timer_token_ack.start()
            if token==get_first_token():
                #Enviar la info dels meus sensors, dormir i tornar a començar
                End_normal=True
                print("Finished")
                #save_parameters()
                com.Switch_to_LoraWan()
                com.savestate()
                #machine.deepsleep(500)

        if timer_token_ack.read()>=5 and token_ack==False:
            print("Estic enviant Token",msg_send)
            com.sendData(msg_send)
            timer_token_ack.reset()
            intent=intent+1
            if intent==10:
                print("he fet més de 10 intents")
                com.change_txpower(get_neighbour_power(node_list.index(id)-2))
                msg_send="Token "+str(token)+" "+str(id)+" "+str(node_list[node_list.index(id)-2])
                intent=1
