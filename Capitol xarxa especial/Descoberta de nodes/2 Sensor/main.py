def check_alarms2(T,temp,tempC,H,dry):
     return False #LLEVAAAAR
     if (int(T>50)+int(temp>50)+int(tempC>50))>=2:
         return True
     if (int(T>30)+int(temp>30)+int(tempC>30))>=2 and H<30 and dry:
         return True
     if T>50 or temp>50 or tempC>50:
        print("Algo malo va a pasar") #mirar els altres :)
    #Falta qualitat d'aire!!
     return False
def save_parameters():
    """
    Save parameters to nv_ram before the deepsleep
    """
    global node_list,neighbours
    for l in range(len(node_list)):
        print(l)
        name="node"+str(l)
        print(name)
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
        return 14

def get_sleeping_time():
    """
    Calculate the time that this node must be in deepsleep mode
    """
    if node_list.index(id)<=(len(node_list)/2)-1:
        time_sleep=periode+periode*node_list.index(id)
    else:
        time_sleep=periode+(len(node_list)-node_list.index(id)-1)*periode
    return time_sleep

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
    while ((len(neighbours[0])<3) & (power<14)): #Potencia max =14
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
        com.change_txpower(get_neighbour_power(node_list.index(id)-1))# envia amb la potencia a la que ha guardat el neighbour al que envia el missatge
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

        if "Alarm" in msg_aux:
            rcv_data=True
            mode=ALARM_MODE
            if "Alarm ok" in msg_aux:
                msg_alarm_ok=msg_aux
            return

        if "Config" in msg_aux and stop_config==False:
                msg=msg_aux
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                splitmsg=msg.split()
                rcv_data=True
                mode=CONFIG_MODE
                return

        if mode==NORMAL_MODE:
            if ("Token" in msg_aux or "Info" in msg_aux):
                rcv_data=True
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
    len_node=pycom.nvs_get("len_node")
    len_neighbours=pycom.nvs_get("len_neighbours")
    node_list=[]
    neighbours=[[],[]]
    for l in range(len_node):
        name="node"+str(l)
        node=pycom.nvs_get(name)
        node_list.append(node)
        print(node_list[l])
    for l in range(len_neighbours):
        name="neighbour"+str(l)
        name2="power"+str(l)
        ids=pycom.nvs_get(name)
        powers=pycom.nvs_get(name2)
        neighbours[0].append(ids)
        neighbours[1].append(powers)
    print(neighbours)
    mode=NORMAL_MODE
    timer_read_sensors.reset()
    timer_read_sensors.start()
    print("Good morning!")

while True:
    if mode==ALARM_MODE:
        if rcv_data:
            rcv_data=False
            splitmsg=msg_alarm_ok.split( )
            msg_alarm=msg_aux
            if "Alarm" in msg_alarm and "ok" not in msg_alarm:
                #Resend the alarm msg
                com.change_txpower(14)
                com.sendData(msg_alarm)
            elif "Alarm ok" in msg_alarm_ok:
                if node_list.index(splitmsg[3])==node_list.index(id): #Alarm ok from:id to:id
                    #Alarm ok ACK. It's for me
                    com.sendData("Alarm ok "+str(id)+" "+str(id))
                    mode=LISTEN_MODE
                    timer_read_sensors.reset()
                    timer_read_sensors.start()
                    msg_alarm=" "
                    msg_alarm_ok=" "
                if msg_alarm_ok and node_list.index(splitmsg[2])==node_list.index(id): #Alarm ok from:id to:id
                    #Pass Alarm ok to other
                    if node_list.index(splitmsg[3])>node_list.index(id):
                        splitmsg[2]=node_list[node_list.index(id)+1]
                    else:
                        splitmsg[2]=node_list[node_list.index(id)-1]
                    msg_alarm=" ".join(splitmsg)
                    com.sendData(str(msg_alarm))
                    msg_alarm_ok=" "
                if id in msg_alarm_ok and splitmsg[3] in msg_alarm_ok:
                    #Alarm ok ACK received, chango to mode LISTEN_MODE
                    mode=LISTEN_MODE
                    timer_read_sensors.reset()
                    timer_read_sensors.start()
                    msg_alarm=" "
                    msg_alarm_ok=" "

        if ("Alarm" in msg_alarm):
            #Resend the alarm msg
            time.sleep(3)
            com.sendData(msg_alarm)

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
                timer_read_sensors.start()
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

        if "Alarm ok" in msg_listen and splitmsg_listen[3]==str(id):
            com.sendData("Alarm ok "+str(id)+" "+str(id))
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
                time.sleep(1)
                msg_listen=" "

            elif isMyACK(int(splitmsg_listen[-1])):    #node_list.index(id)<int(splitmsg[-1]):
                print("Discover Finished")
                mode=NORMAL_MODE
                timer_Disc_end.reset()
                timer_Disc_end.stop()
                discover_end_ack=True
                neighbours=com.neighbours_min(neighbours,neighbours_aux)

        elif "Token" in msg_listen and id in msg_listen:
            mode=NORMAL_MODE
            timer_Disc_end.reset()
            timer_Disc_end.stop()
            discover_end_ack=True
            intent=1
            token_ack=False
            info_ack=True
            info_passed=False
            neighbours=com.neighbours_min(neighbours,neighbours_aux)

            rcv_data=True#Repasar això

        if discover_end_ack==False and timer_Disc_end.read()>5:
            #Resend the msg to ask again an ACK
            com.sendData(str(msg_send))
            timer_Disc_end.reset()

    if mode==NORMAL_MODE:
        if timer_read_sensors.read()>=5:
            print("Llegir sensors")
            readen=True
            T=47+machine.rng()%6
            temp=47+machine.rng()%6
            tempC=47+machine.rng()%6
            H=30-machine.rng()%1
            dry=True
            dhi=1
            alarma=check_alarms2(T,temp,tempC,H,dry)
            if alarma==True:
                print("Hi ha alarma")
                mode=ALARM_MODE
                # packet_tbmp = ustruct.pack('f',temp)
                # packet_tempC = ustruct.pack('f',tempC)
                # packet_dhi = ustruct.pack('b',dhi)
                # #packet_val = ustruct.pack('H',val)
                # #packet_dust = ustruct.pack('f',dustDensity)
                # packet_Tht = ustruct.pack('f',T)
                # packet_Hht = ustruct.pack('H',round(H*100))
                msg_alarm="Alarm "+str(id)+" "+str(id)+" 150 "+str(tempC)+" "+str(T)+" "+str(H)+" "+str(temp)+" "+"0"+" "+"1"
                com.sendData(msg_alarm)
            timer_read_sensors.reset()
        if rcv_data==True:
            rcv_data=False
            msg=msg_aux
            print("normal missatge : ",msg)
            if type(msg)==bytes:
                msg=bytes.decode(msg)
            splitmsg=msg.split()
            #Per la trama de Info les posicions no són iguals
                #Trama info= Info, id de qui es la info,id de a qui va el missatge, informació
                #splitmsg[1]=Node de la info
                #splitmsg[2]=Node que ho ha de reenviar
                #splitmsg[3]=info
                #Quan es reenvia l'info la funció ha de ser alreves!
            if "Info" in msg:
                if info_ack==False: #Waiting for info_ack
                    print("nodes1: ",node_seguent,node_anterior,node_seguent2)
                    if ("Info ok" in msg) or (splitmsg[1]==id) or (splitmsg[2]==node_seguent2):
                        info_ack=True
                        token_ack=True
                        if info_passed==True:
                            print("Info enviada")
                            #save_parameters()
                            #machine.deepsleep(get_sleeping_time())
                elif info_ack==True:
                    if splitmsg[2]==id:
                        node_anterior,node_seguent,node_seguent2=get_next_node(splitmsg[2],splitmsg[1])
                        print("Passar info a un altre nodes2: ",node_seguent,node_anterior,node_seguent2)
                        if splitmsg[1]==node_anterior:
                            token_ack=True# Si el node que envia la info es el seguent a tu no reenviara el token i l'ack serà info

                        #Trama info= Info, id de qui es la info,id de a qui va el missatge, informació
                        #token_ack=False
                        #msg_send=splitmsg
                        splitmsg[2]=node_list[node_list.index(node_seguent)]
                        msg=" ".join(splitmsg)
                        com.change_txpower(get_neighbour_power(node_list.index(node_seguent)))
                        com.sendData(str(msg))
                        print("he enviat info de un altre", msg)
                        #node_seguent2_aux=node_seguent2
                        msg_retry=msg
                        info_ack=False
                        intent=1

            #Trama del token= "Token, node destinatari, node que esta enviant, node a qui ho envia(el node que ho ha de reenviar)"
            #splitmsg[1]=Node destinatari del token
            #splitmsg[2]=Node enviant
            #splitmsg[3]=Node que ho ha de reenviar
            #Trama info= Info, id de qui es la info,id de a qui va el missatge, informació
            #splitmsg[1]=Node de la info
            #splitmsg[2]=Node que ho ha de reenviar
            #splitmsg[3]=info
            #(node_destinatari,node_enviant)
            if "Token" in msg and info_ack==True:
                node_anterior,node_seguent,node_seguent2=get_next_node(splitmsg[3],splitmsg[2])
                # print("Token" in msg and splitmsg[2]==node_anterior)
                # print(msg,splitmsg,node_anterior)
                if splitmsg[3]==id:
                    print("Missatge de token per jo")
                    if splitmsg[1]==id:
                        if readen: #LLevar quan funcioni llegir
                            info_passed=True
                            #llegir els sensors

                            llista="150"+" "+str(tempC)+" "+str(T)+" "+str(H)+" "+str(temp)+" "+"0"+" "+"1"
                            #llista="150"+" "+"23"+" "+"24"+" "+"40"+" "+"25"+" "+"0"+" "+"1"
                            #splitmsg[2] és qui t' està enviant i a qui li has de retornar la info
                            msg_retry="Info"+" "+ str(id)+" "+splitmsg[2]+" "+llista
                            com.sendData(msg_retry)
                            print("he enviat info",msg_retry)
                            timer3.reset()
                            timer3.start()
                            info_ack=False
                            token_ack=True
                        else: #llegir quan funcioni llegir
                            print("No he llegit sensors")
                    else:
                        print("He de passar es token a un altre")
                        msg_send=splitmsg[:]
                        msg_send[2]=str(id)
                        msg_send[3]=str(node_seguent)
                        msg_retry=" ".join(msg_send)
                        com.change_txpower(get_neighbour_power(node_list.index(node_seguent)))
                        com.sendData(msg_retry)
                        print("estic enviant", msg_retry)
                        token_ack=False
                        timer3.reset()
                        #msg_retry=msg_send
                elif splitmsg[1]==node_seguent:
                    token_ack=True

        if token_ack==False or info_ack==False:
            if timer3.read()>=3:
                com.sendData(msg_retry)
                print("He reenviat ", msg_retry)
                timer3.reset()
                intent=intent+1
                if intent==3 and (node_list.index(id)!=1 or node_list.index(id)!=len(node_list)-2):
                    com.change_txpower(get_neighbour_power(node_list.index(node_seguent2)))
                    splitmsg=msg_retry.split( )
                    if "Info" in msg_retry:
                        splitmsg[2]=node_list[node_list.index(node_seguent2)]
                        msg_retry=" ".join(splitmsg)
                        print("Canvi de node, msg: ",msg_retry)
                    elif "Token" in msg_retry:
                        #node_anterior,node_seguent,node_seguent2=get_next_node(splitmsg[2],splitmsg[3])
                        msg_send[3]=str(node_seguent2)
                        msg_retry=" ".join(msg_send)
                        node_seguent=node_seguent2
                        print("Canvi de node, msg: ",msg_retry)
                    intent=1
                        #demanarTomeu?????????????????????
    if mode==DISCOVER_MODE:
        print("Discoveeeer")
        discover(id)
        missatge=False
        #end_discover=False
        mode=LISTEN_MODE
        timer_read_sensors.start()
