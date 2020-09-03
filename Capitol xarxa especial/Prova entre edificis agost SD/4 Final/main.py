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

def saveFileMsgs(neighbours,rtc):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) counter(int) table([id][tx_power])
        Output: 1 file
        Example: 15/10/2019 13:21:31 5
                 id2 min_pow, id3 max_pow
        '''
        f = open('/sd/neighbours_final.txt', 'a')
        f.write("{}/{}/{} {}:{}:{}".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
        for i in range(len(neighbours[0])):
            f.write("id {} pow {} , ".format(neighbours[0][i],neighbours[1][i]))
        f.write("\n")
        f.close()
        return

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
        return 14
def get_next_node(node_destinatari,node_enviant):
    """
    Find 2 nodes to send some msg taking into account the sense of the path
    """
    if node_list.index(node_destinatari)>node_list.index(node_enviant):
        #sentit="up"
        node_anterior=node_list[node_list.index(id)-1]
        node_seguent=node_list[node_list.index(id)-2]
        if node_list.index(id)-3 < len(node_list):
            node_seguent2=node_list[node_list.index(id)-3]
        else:
            node_seguent2=node_seguent
    else:
        return(id,id,id)
    print("Get_next_node ",node_destinatari,node_enviant," result ",node_anterior,node_seguent,node_seguent2)
    return(node_anterior,node_seguent,node_seguent2)

def discover(id):
    global Hello_received,End_discover
    global neighbours,rtc,f
    print("Discovering")
    power=2 #min
    com.change_txpower(power)

    while ((len(neighbours[0])<3) & (power<14)): #Potencia max =14
        print("I'm in")
        #Enviar missatge inici de descoberta
        msg_tx='Discover normal %i %s'%(power,str(id))
        for i in range(4):
            msg=aux
            com.sendData(str(msg_tx),rtc,f)
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
        com.sendData(str(msg_retry),rtc,f)
        time.sleep(5)
        print(msg_retry)

    End_discover=False
    print("He acabat discover",neighbours)
    saveFileMsgs(neighbours,rtc)
    return

def interrupt(lora):
    print("Interrupcio")
    global rcv_data
    global msg, aux, error,msg_alarm_ok
    global mode, rtc,f
    global Hello_received, End_discover, stop_config

    aux=com.reciveData(rtc,f)
    if aux!="error":
        if "Alarm" in aux:
            if len(node_list)>0:
                rcv_data=True
                mode=ALARM_MODE
            if "Alarm ok" in aux:
                msg_alarm_ok=aux
            if mode==CONFIG_MODE:
                com.sendData(msg_alarm_ok,rtc,f)
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
            f = open('/sd/process_final.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} Empieza el config\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
            f.close()

        if mode==NORMAL_MODE:
            if ("Token" in aux or "Info" in aux):
                rcv_data=True
                return
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

while rtc.now()[3]<hora+5:

    if mode==CHECK:
        com.change_txpower(14)
        com.sendData("Hay buena cobertura con la residencia "+str(i),rtc,f)
        i=i+1
        if i>50:
            i=0
        time.sleep(4)
        if "Config" in msg:
            mode=CONFIG_MODE
            f = open('/sd/process_final.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} Empieza el config\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
            f.close()

    if mode==ALARM_MODE:
        if rcv_data:
            rcv_data=False
            msg_alarm=aux
            splitmsg=msg_alarm.split( )
            if "Alarm" in msg_alarm and "ok" not in msg_alarm:
                #Resend the alarm msg
                com.change_txpower(14)
                com.sendData(msg_alarm,rtc,f)
            elif "Alarm ok" in msg_alarm:
                if splitmsg[3]==str(node_list.index(id)):
                    msg_alarm="Alarm ok "+str(node_list.index(id))+" "+str(node_list.index(id))
                    com.sendData(str(msg_alarm),rtc,f)
                    #Alarm ok ACK received, chango to mode LISTEN_MODE
                    config_ACK=False
                    config_start=True
                    power=2
                    rcv_data=False
                    intent=1
                    nummissatges=1
                    node_list=[]
                    neighbours=[[],[]]
                    neighbours_aux=[[],[]]
                    msg="Config 2"
                    node_list=""
                    msg_alarm=" "
                    error=False
                    Hello_received=False
                    End_discover=False
                    info_passed=False
                    stop_config=False
                    mode=CONFIG_MODE
                    #machine.deepsleep((period*60*1000)+200)
        if ("Alarm" in msg_alarm):
            #Resend the alarm msg
            time.sleep(30)
            com.sendData(msg_alarm,rtc,f)

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
                #time.sleep(3+machine.rng()%1)
                msg=msg+" "+str(id)
                com.sendData(msg,rtc,f)
                print("Enviare: ",msg)
                config_start=False
                if type(msg)==bytes:
                    msg=bytes.decode(msg)
                if node_list=="" and "Config" in msg:
                    splitmsg=msg.split( )
                    node_list=splitmsg[2:]
                timer.start()
                while timer.read()<30:
                    if rcv_data==True and id not in msg:
                        if type(msg)==bytes:
                            msg=bytes.decode(msg)
                        splitmsg=msg.split( )
                        node_list2=splitmsg[2:]
                        if node_list2!=node_list:
                            timer.reset()
                            timer.start()
                            if len(node_list2)>len(node_list):
                                node_list=node_list2
                            elif len(node_list2)==len(node_list) and id not in node_list2:
                                msg=msg+" "+str(id)
                                if type(msg)==bytes:
                                    msg=bytes.decode(msg)
                                splitmsg=msg.split( )
                                node_list2=splitmsg[2:]
                                node_list=node_list2
                        time.sleep(2)
                        rcv_data=False
                        com.sendData(msg,rtc,f)

                timer.reset()
                timer.stop()
                com.get_node_list(node_list)
                f = open('/sd/process_final.txt', 'a')
                f.write("{}/{}/{} {}:{}:{} Tenemos node_list {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],node_list))
                f.close()
                msg="stop "+str(power)+" "+str(" ".join(node_list))+" "+str(node_list.index(id))
                com.sendData(msg,rtc,f)
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
                f=open('/sd/msg_received_final.txt','a')
                f.write("{}/{}/{} {}:{}:{} Config ack recibido \n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
                f.close()
                mode=DISCOVER_MODE
                config_start=False
                print("He acabat el config")


        #print("Part 3 ",config_ACK, config_start)
        if config_ACK==False and config_start==False:
            if intent<3:
                com.sendData(msg_retry,rtc,f)
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
        f = open('/sd/process_final.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} Empieza discover\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
        f.close()
        discover(id)
        f = open('/sd/process_final.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} Acaba discover\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5]))
        f.close()
        mode=LISTEN_MODE
        print("End my discover")
        timer_read_sensors.start()
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
                    com.sendData("Hello "+ str(pow) + " "+ str(id),rtc,f)
                    neighbours_aux=com.update_neighbours(pow,id_n,neighbours_aux)
                elif "Discover end" in msg and isMyTurn(int(msg[-1])): #All discovers finished
                    neighbours=com.neighbours_min(neighbours,neighbours_aux)
                    rcv_data=False
                    splitmsg_send=msg.split()
                    turn=int(splitmsg_send[-1])+1
                    splitmsg_send[-1]=str(turn)
                    msg_send=" ".join(splitmsg_send)
                    com.sendData(str(msg_send),rtc,f)
                    print("Sending: ",msg_send)
                    timer_Disc_end.start()
                    time.sleep(1)
                    msg=" "
                elif "Discover end" in msg and isMyACK(int(splitmsg[-1])) or "Token" in msg:    #node_list.index(id)<int(splitmsg[-1]):
                    print("Discover Finished")
                    mode=NORMAL_MODE
                    timer_Disc_end.reset()
                    timer_Disc_end.stop()
                    discover_end_ack=True
                    neighbours=com.neighbours_min(neighbours,neighbours_aux)
                    saveFileMsgs(neighbours,rtc)

                elif "Token" in msg and id in msg:
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
                com.sendData(str(msg_send),rtc,f)
                print("Sending again Discover end")
                timer_Disc_end.reset()
    if mode==NORMAL_MODE:
        if timer_read_sensors.read()>=60:
            print("Llegir sensors")
            readen=True
            T=47+machine.rng()%6
            temp=47+machine.rng()%6
            tempC=47+machine.rng()%6
            H=30-machine.rng()%1
            dry=True
            dhi=1
            alarma=check_alarms2(T,temp,tempC,H,dry)
            if alarma==True or nummissatges==4:
                print("Hi ha alarma")
                mode=ALARM_MODE
                msg_alarm="Alarm "+str(id)+" "+str(id)+" 150 "+str(tempC)+" "+str(T)+" "+str(H)+" "+str(temp)+" "+"0"+" "+"1"
                com.sendData(msg_alarm,rtc,f)
                nummissatges=0
            timer_read_sensors.reset()
        if rcv_data==True:
            rcv_data=False
            msg=aux
            print("normal missatge : ",msg)
            if type(msg)==bytes:
                msg=bytes.decode(msg)
            splitmsg=msg.split()
            #Per la trama de Info les posicions no són iguals
                #Trama info= Info, id de qui es la info,id de a qui va el missatge, informació
                #splitmsg[1]=Node de la info
                #splitmsg[2]=Node que ho ha de"{^���r*(�("��[�����r�ޮ۫i�'��^��ߊV��m� reenviar
                #splitmsg[3]=info
                #Quan es reenvia l'info la funció ha de ser alreves!
            if "Info" in msg:
                if info_ack==False: #Waiting for info_ack
                    print("nodes1: ",node_seguent,node_anterior,node_seguent2)
                    if ("Info ok" in msg):# or (splitmsg[1]==id) or (splitmsg[2]==node_seguent2):
                        info_ack=True
                        token_ack=True
                        if info_passed==True:
                            print("Info enviada")
                            nummissatges=nummissatges+1
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
                        com.sendData(str(msg),rtc,f)
                        print("he enviat info de un altre", msg)
                        #node_seguent2_aux=node_seguent2
                        msg_retry=msg
                        info_ack=False
                        intent=1

            #Trama del token= "Token, node destinatari, node que esta enviant, node a qui ho envia(el node que ho ha de reenviar)"
            #splitmsg[1]=Node destinatari del token
            #splitmsg[2]=Node enviant (principi o final)
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
                            msg_retry="Info"+" "+ str(id)+" "+str(node_anterior)+" "+llista
                            com.sendData(msg_retry,rtc,f)
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
                        com.sendData(msg_retry,rtc,f)
                        print("estic enviant", msg_retry)
                        token_ack=False
                        timer3.reset()
                        #msg_retry=msg_send
                elif splitmsg[1]==node_seguent:
                    token_ack=True

        if token_ack==False or info_ack==False:
            if timer3.read()>=30:
                com.sendData(msg_retry,rtc,f)
                print("He reenviat ", msg_retry)
                timer3.reset()
                intent=intent+1
                if intent==3 and (node_list.index(id)!=1 or node_list.index(id)!=len(node_list)-2):
                    com.change_txpower(get_neighbour_power(node_list.index(node_seguent)))
                    splitmsg=msg_retry.split( )
                    if "Info" in msg_retry:
                        splitmsg[2]=node_list[node_list.index(node_seguent)]
                        msg_retry=" ".join(splitmsg)
                        print("Canvi de node, msg: ",msg_retry)
                    elif "Token" in msg_retry:
                        #node_anterior,node_seguent,node_seguent2=get_next_node(splitmsg[2],splitmsg[3])
                        msg_send[3]=str(node_seguent2)
                        msg_retry=" ".join(msg_send)
                        node_seguent=node_seguent2
                        print("Canvi de node, msg: ",msg_retry)
                    intent=1
