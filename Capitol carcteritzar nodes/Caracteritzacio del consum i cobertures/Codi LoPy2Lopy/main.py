def saveFileMsgs(msg,counter,rtc):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) counter msg
        Example: 15/10/2019 13:21:31 30
        '''
        #Write the image temp in data.txt
        f = open('msgs_node.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} counter {} msg{}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],counter,msg))
        f.close()
        return
def saveFileParticulas(rtc,sensorQAire,sensorHPMA10,sensorHPMA25):
        '''
        Format of the data: date (DD/MM/YYYY HH:MM:SS) sensorQAire, pm10m, pm2.5
        Example: 15/10/2019 13:21:31
        '''
        #Write the image temp in data.txt
        f = open('node_particulas.txt', 'a')
        f.write("{}/{}/{} {}:{}:{} {} {} {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],sensorQAire,sensorHPMA10,sensorHPMA25))
        f.close()
        return

com=com.Comunication()
com.start_LoraRaw()
periode=2*60  #min
print("Start")
i=0
for i in range(300):
    p_out.value(1)
    time.sleep(0.5)
    p_out.value(0)

    com.change_txpower(2)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")#packet_dust+packet_tempC+packet_Tht+packet_Hht+packet_tbmp+packet_val+packet_dhi+packet_T_cam+id_aux+ustruct.pack('H',counter)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    com.change_txpower(4)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    com.change_txpower(6)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    com.change_txpower(8)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    com.change_txpower(10)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    com.change_txpower(12)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")
    p_out.value(1)
    time.sleep(0.9)
    p_out.value(0)

    com.change_txpower(14)
    com.sendData("255 23 24 30 24 1 26 30aea458f2e4 0")
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)
    time.sleep(periode)
    print("Time sleep finished")
