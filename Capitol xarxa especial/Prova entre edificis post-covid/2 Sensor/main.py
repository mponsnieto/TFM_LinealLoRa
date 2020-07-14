
def saveFileMsgs(neighbours,counter,rtc):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) counter(int) table([id][tx_power])
        Output: 2 files
        Example: 15/10/2019 13:21:31 5
                 id2 min_pow, id3 max_pow
        '''
        f = open('dates_middle.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} counter {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter))
        f.close()

        f = open('neighbours_middle.txt', 'a')
        for i in range(len(neighbours[0])):
            f.write("id {} pow{}, ".format(neighbours[0][i],neighbours[1][i]))
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
        return 14

def get_sleeping_time():
    """
    Calculate the time that this node must be in deepsleep mode
    """
    # if node_list.index(id)<=(len(node_list)/2)-1:
    #     time_sleep=periode+periode*node_list.index(id)
    # else:
    #     time_sleep=periode+(len(node_list)-node_list.index(id)-1)*periode
    return 5.2*60*1000

def isMyTurn(token):
    #The token is for me
    return node_list.index(id)==token

def isMyACK(token):
    return node_list.index(id)<token

def get_next_node(node_destinatari,node_enviant):
    """
    Find 2 nodes to send some msg taking into account the sense of the path
    """
    if node_list.index(node_destinatari)>node_list.index(node_enviant):
        #sentit="up"
        node_anterior=node_list[node_list.index(id)-1]
        node_seguent=node_list[node_list.index(id)+1]
        if node_list.index(id)+2 < len(node_list):
            node_seguent2=node_list[node_list.index(id)+2]
        else:
            node_seguent2=node_seguent
    elif node_list.index(node_destinatari)<node_list.index(node_enviant):
        #sentit="down"
        node_anterior=node_list[node_list.index(id)+1]
        node_seguent=node_list[node_list.index(id)-1]
        if node_list.index(id)-2 >= 0:
            node_seguent2=node_list[node_list.index(id)-2]
        else:
            node_seguent2=node_seguent
    else:
        return(id,id,id)
    print("Get_next_node ",node_destinatari,node_enviant," result ",node_anterior,node_seguent,node_seguent2)
    return(node_anterior,node_seguent,node_seguent2)

def discover(id):
    global end_discover
    print("Discovering")
    power=2 #min
    com.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868,tx_power=power)
    global neighbours
    while ((len(neighbours[0])<2) & (power<14)): #Potencia max =14
        #Enviar missatge inici de descoberta
        msg_tx='Discover normal %i %s'%(power,id)
        for i in range(4):
            msg=msg_aux
            com.sendData(str(msg_tx))
            print("Msg sent: ",msg_tx)

            #Wait to receive answers
            time.sleep(2.5+ machine.rng()%1)
            if "Hello" in msg:
                try:
                    splitmsg=msg.split( )
                    id_n=splitmsg[2]
                    pow=int(splitmsg[1])
                    print("Update neighbours")
                    neighbours=com.update_neighbours(pow,id_n,neighbours)
                except Exception as e:
                    print(e)

        #change power
        print(power)
        power=power+1
        com.change_txpower(power)

    #Send next token
    msg_retry='Discover next %i %s'%(power,node_list.index(id)-1)
        #Wait for ACK
    while end_discover==False:
        com.change_txpower(get_neighbour_power(node_list.index(id)-1))
        com.sendData(str(msg_retry))
        print("he enviat", msg_retry)
        time.sleep(5)
    print("Discover finished: ",neighbours)
    end_discover=False
    return

def interrupt(lora):
    global rcv_data
    global msg, splitmsg, msg_aux,msg_alarm_ok
    global mode
    global stop_config, config_start, end_discover
    global splitmsg_stop
    global node_list
    print("interrupcio")
    lora.power_mode(LoRa.ALWAYS_ON)

    msg_aux=com.reciveData()
    if msg_aux!="error":
        if "Config" in msg_aux and stop_config==False:
                msg=msg_aux
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                splitmsg=msg.split()
                rcv_data=True
                mode=CONFIG_MODE
                return

        if (mode==CONFIG_MODE or mode==LISTEN_MODE) and "stop" in msg_aux:
            #Config has finished
            msg=msg_aux
            print("Stop msg received")
            rcv_data=True
            stop_config=True
            if type(msg)==bytes:
                msg=bytes.decode(msg)
            splitmsg=msg.split()
            splitmsg_stop=splitmsg[:]
            #Save the node_list
            node_list=splitmsg[2:-1]

            if mode==LISTEN_MODE and node_list.index(id)+1==int(splitmsg[-1]):
                power=14
                com.change_txpower(power)
                splitmsg[-1]=str(node_list.index(id))
                msg=" ".join(splitmsg)
                com.sendData(str(msg))
                print("Stop msg sent")
            return

        if mode==LISTEN_MODE:
            rcv_data=True
            return

        if mode==DISCOVER_MODE:
            if type(msg_aux)==bytes:
                msg_aux=bytes.decode(msg_aux)
            if "Discover normal" in msg_aux:
                msg=msg_aux
                end_discover=True
            return
    else:
        print("Receiving error")

###############################################################################
                                   #MAIN
###############################################################################

com.lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868,tx_power=power)
com.lora.callback(trigger=(LoRa.RX_PACKET_EVENT), handler=interrupt)
reset_cause=machine.reset_cause()
if reset_cause==machine.DEEPSLEEP_RESET:
    node_list=[]
    neighbours=[[],[]]
    mode=LISTEN_MODE
    counter=pycom.nvs_get("count")
    print("Good morning!")

while True:
    if mode==CONFIG_MODE:
        if rcv_data and id not in msg and stop_start==False:
            rcv_data=False
            config_start=True
            print("el missatge es: ", msg)
            print(id not in msg)
            try:
                splitmsg=msg.split( )
                id_n=splitmsg[-1]
                pow=int(splitmsg[1])
                com.change_txpower(power)
                msg_retry= msg+" "+str(id)
                print("Enviare: ",msg+" "+str(id))
                com.sendData(msg_retry)
            except Exception as e:
                print(e)
        if (rcv_data==True) and (id in msg):
            rcv_data=False
            if "stop" in msg:
                splitmsg=msg.split( )
                if node_list.index(id)+1==int(splitmsg[-1]):
                    splitmsg[-1]=str(node_list.index(id))
                    msg=" ".join(splitmsg)
                    com.sendData(str(msg))
                    msg_retry=msg
                    print("Stop msg sent")
                    stop_start=True
                    stop_ACK=False
                    time.sleep(2)
            elif "Config" in msg:
                print("Config ACK received")
                #ack=True
                config_ACK=True
                splitmsg=msg.split( )
                id_n=splitmsg[-1]
                pow=int(splitmsg[1])
        if stop_ACK==False and stop_start==True:
            if node_list.index(id)-1>=int(splitmsg_stop[-1]):
                config_start=False
                print("Stop finished")
                stop_ACK=True
                mode=LISTEN_MODE

        if (config_ACK==False and config_start==True) or (stop_start==True and stop_ACK==False):
            if intent<3:
                #msg stop es el missatge normal de config o el de stop
                com.sendData(msg_retry)

                #print("Enviare %s intent: "%(intent),msg+" "+str(id))
                print("Enviare intent: ", msg_retry)
                time.sleep(2+ machine.rng()%2.5)
                intent=intent+1
            elif power<14: #Max power=14
                intent=1
                power=power+1
                if (type(msg_retry)==bytes):
                    msg_retry=bytes.decode(msg_retry)
                    print("decode msg", msg_retry)
                print(msg_retry)
                splitmsg=msg_retry.split( )
                splitmsg[1]=str(power)
                msg_retry=" ".join(splitmsg)
                com.change_txpower(power)
            else:
                power=2
                intent=1
                com.change_txpower(power)

    if mode==LISTEN_MODE:
        missatge=False
        if (rcv_data==True):
            msg_listen=msg_aux

            if type(msg_aux)==bytes:
                msg=bytes.decode(msg_aux)
            splitmsg_listen=msg_listen.split()

            rcv_data=False
            missatge=True

        if "Discover normal" in msg_listen and missatge==True:
            missatge=False
            id_n=splitmsg_listen[-1]
            pow=int(splitmsg_listen[2])
            com.change_txpower(power)
            print("Enviare", "Hello ",pow , " ", id )
            time.sleep(machine.rng()%2)
            com.sendData("Hello "+ str(pow) + " "+ str(id))
            neighbours_aux=com.update_neighbours(pow,id_n,neighbours_aux)

        elif "Discover" and "next" in msg_listen:
            if isMyTurn(int(msg_listen[-1]))==True:#Aqui podriem usar msg_aux directament?
                mode=DISCOVER_MODE
                msg_listen=" "

        elif "Discover end" in msg_listen:
            if isMyTurn(int(msg_listen[-1])):
                splitmsg_send=splitmsg_listen[:]
                turn=int(splitmsg_listen[-1])+1
                splitmsg_send[-1]=str(turn)
                msg_send=" ".join(splitmsg_send)
                com.sendData(str(msg_send))
                print("Sending: ",msg_send)
                timer_Disc_end.start()
                time.sleep(1)
                msg_listen=" "

            elif isMyACK(int(splitmsg_listen[-1])):    #node_list.index(id)<int(splitmsg[-1]):
                print("Discover Finished")
                mode=NORMAL_MODE
                timer_Disc_end.reset()
                timer_Disc_end.stop()
                discover_end_ack=True
                neighbours=com.neighbours_min(neighbours,neighbours_aux)
                saveFileMsgs(neighbours,counter,rtc)
                counter=counter+1
                print("DeepSleep ",counter)
                pycom.nvs_set("count",counter)
                machine.deepsleep((period*60*1000)+200) #5.2min, machine.deepsleep([time_ms])

        if discover_end_ack==False and timer_Disc_end.read()>5:
            #Resend the msg to ask again an ACK
            com.sendData(str(msg_send))
            print("Sending again Discover end")
            timer_Disc_end.reset()

    if mode==DISCOVER_MODE:
        print("Discover")
        discover(id)
        missatge=False
        #end_discover=False
        mode=LISTEN_MODE
