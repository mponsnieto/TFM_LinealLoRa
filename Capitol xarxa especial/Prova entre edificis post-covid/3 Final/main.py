
def saveFileMsgs(neighbours,counter,rtc):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) counter(int) table([id][tx_power])
        Output: 2 files
        Example: 15/10/2019 13:21:31 5
                 id2 min_pow, id3 max_pow
        '''
        f = open('dates_final.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} counter {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter))
        f.close()

        f = open('neighbours_final.txt', 'a')
        for i in range(len(neighbours[0])):
            f.write("id {} pow {} , ".format(neighbours[0][i],neighbours[1][i]))
        f.write("\n")
        f.close()
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


def discover(id):
    global Hello_received,End_discover
    global neighbours
    print("Discovering")
    power=2 #min
    com.change_txpower(power)

    while ((len(neighbours[0])<2) & (power<14)): #Potencia max =14
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
    com.start_LoraRaw()
    node_list=[]
    neighbours=[[],[]]
    mode=LISTEN_MODE
    counter=pycom.nvs_get("count")
    print("Good morning!")

else:
    com.start_LoraRaw()

com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
com.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868,tx_power=power)

while True:
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
                msg=msg+" "+str(id)
                com.sendData(msg)
                print("Enviare: ",msg)
                config_start=False
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                if node_list=="":
                    splitmsg=msg.split( )
                    node_list=splitmsg[2:]
                timer.start()
                while timer.read()<6:
                    if rcv_data==True and id not in msg:
                        msg=msg+" "+str(id)
                        com.sendData(msg)
                        if type(msg)==bytes:
                            msg=bytes.decode(msg)
                        splitmsg=msg.split( )
                        node_list2=splitmsg[2:]
                        if node_list2!=node_list:
                            timer.reset()
                            timer.start()
                            if len(node_list2)>len(node_list):
                                node_list=node_list2


                com.get_node_list(node_list)
                msg="stop "+str(power)+" "+str(" ".join(node_list))+" "+str(node_list.index(id))
                com.sendData(msg)
                msg_retry=msg
                splitmsg=msg.split( )
                print("Enviare: ",msg)
                #time.sleep(5)

        #print("Part 2 ",msg,rcv_data,id in msg)
        if (rcv_data==True) and (id in msg) and ("stop" in msg) and (error==False):
            if int(msg.split()[-1])<node_list.index(id):
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
            if len(node_list)>0:
                if ("Discover normal") in msg: #Other node is discovering
                    id_n=splitmsg[-1]
                    pow=int(splitmsg[2])
                    com.change_txpower(pow)
                    print("Enviare", "Hello ",pow , " ", id )
                    time.sleep(machine.rng()%2)
                    com.sendData("Hello "+ str(pow) + " "+ str(id))
                    neighbours_aux=com.update_neighbours(pow,id_n,neighbours_aux)
                elif "Discover end" in msg and isMyTurn(int(msg[-1])): #All discovers finished
                    neighbours=com.neighbours_min(neighbours,neighbours_aux,id)
                    rcv_data=False
                    splitmsg_send=msg.split()
                    turn=int(splitmsg_send[-1])+1
                    splitmsg_send[-1]=str(turn)
                    msg_send=" ".join(splitmsg_send)
                    com.sendData(str(msg_send))
                    print("Sending: ",msg_send)

    #------------------------Chapuza per aquesta prova--------------------------
                    time.sleep(5)
                    com.sendData(str(msg_send))
                    time.sleep(5)
                    com.sendData(str(msg_send))
    #------------------------Fi de chapuza per aquesta prova--------------------

                    saveFileMsgs(neighbours,counter,rtc)
                    counter=counter+1
                    print("DeepSleep ",counter)
                    pycom.nvs_set("count",counter)
                    machine.deepsleep(period*60*1000) #5min, machine.deepsleep([time_ms])
