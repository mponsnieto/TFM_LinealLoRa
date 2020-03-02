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


periode=0.5*60  #min
print("Start")
i=0
for i in range(300):
    p_out.value(1)
    time.sleep(0.5)
    p_out.value(0)
    #Sensor PT BMP085
    tbmp = bmp.GetTemperature
    packet_tbmp= ustruct.pack('H',int(tbmp))
    # dataBMP="Temp: %0.2f *C" % (temp)
    # print(dataBMP)
    bmp.saveFile(tbmp,rtc)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    # #Sensor T MCP
    tempC = mcp.GetTemperature
    packet_tempC= ustruct.pack('H',int(tempC))
    #dataMCP='Temperature: {} C '.format(tempC)
    #print(dataMCP)
    mcp.saveFile(tempC,rtc)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    #Sensor HS
    val,dry,humid,inWater=sensorHSol.CalcularHumitat()
    dhi=dry+humid*2+inWater*3
    packet_val= ustruct.pack('H',int(val))
    packet_dhi= ustruct.pack('B',int(dhi))
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    #Sensor QAire/ Particules
    pm10, pm25 = pma.read_particules()
    dustDensity=sensorQAire.CalculateDust()
    # packet_dust= ustruct.pack('H',int(dustDensity))
    packet_dust= ustruct.pack('H',int(pm10))
    #print("DustDensity: ",dustDensity," ug/m3")
    saveFileParticulas(rtc,pm25,pm10,dustDensity)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    #Càmera
    T_cam=cam.readTemp
    packet_T_cam= ustruct.pack('H',int(T_cam))
    # print("T from thermistor= %0.2f *C" % (Temp))
    Tcam=cam.readPixels
    # print("Image readen pixel by pixel in *C")
    # for i in range(8): print(T[i])
    cam.saveFile(Tcam,T_cam,rtc)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    #Sensor HT
    T_ht=SensorHT.readTemperature()
    SensorHT.saveFile(T_ht,rtc)
    H_ht=SensorHT.readHumidity()
    packet_Tht= ustruct.pack('H',int(T_ht))
    packet_Hht= ustruct.pack('B',round(int(H_ht)))
    p_out.value(1)
    time.sleep(0.9)
    p_out.value(0)

    print("Sending to node...")
    com.sendData(str(pm10+tempC+T_ht+H_ht+tbmp+val+dhi+T_cam))
    saveFileMsgs(str(pm10)+" "+str(tempC)+" "+str(T_ht)+" "+str(H_ht)+" "+str(tbmp)+" "+str(val)+" "+str(dhi)+" "+str(T_cam)+" "+str(id),"1",rtc)
    #print("Counter of msg: ",counter)
    #counter=counter+1
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)
    time.sleep(periode)
    print("Time sleep finished")
