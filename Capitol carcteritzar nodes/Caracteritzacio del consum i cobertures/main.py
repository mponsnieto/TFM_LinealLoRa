com=com.Comunication()
com.JoinLoraWan()
periode=5*60  #min
print("Start")
i=0
for i in range(600):
    p_out.value(1)
    time.sleep(0.5)
    p_out.value(0)
    #Sensor PT BMP085
    temp = bmp.GetTemperature
    packet_tbmp= ustruct.pack('H',int(temp))
    # dataBMP="Temp: %0.2f *C" % (temp)
    # print(dataBMP)
    #bmp.saveFile(temp,rtc)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    # #Sensor T MCP
    tempC = mcp.GetTemperature
    packet_tempC= ustruct.pack('H',int(tempC))
    #dataMCP='Temperature: {} C '.format(tempC)
    #print(dataMCP)
    #mcp.saveFile(tempC,rtc)
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
    # dustDensity=sensorQAire.CalculateDust()
    # packet_dust= ustruct.pack('H',int(dustDensity))
    packet_dust= ustruct.pack('H',int(pm10))
    #print("DustDensity: ",dustDensity," ug/m3")
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    #Càmera
    Temp=cam.readTemp
    packet_T_cam= ustruct.pack('H',int(Temp))
    # print("T from thermistor= %0.2f *C" % (Temp))
    T=cam.readPixels
    # print("Image readen pixel by pixel in *C")
    # for i in range(8): print(T[i])
    #cam.saveFile(T,Temp,rtc)
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)

    #Sensor HT
    T=SensorHT.readTemperature()
    #SensorHT.saveFile(T,rtc)
    H=SensorHT.readHumidity()
    packet_Tht= ustruct.pack('H',int(T))
    packet_Hht= ustruct.pack('B',round(int(H)))
    p_out.value(1)
    time.sleep(0.9)
    p_out.value(0)

    print("Sending to GTW...")
    com.EnviarGateway(packet_dust+packet_tempC+packet_Tht+packet_Hht+packet_tbmp+packet_val+packet_dhi+packet_T_cam+id_aux)
    print("Counter of msg: ",counter)
    counter=counter+1
    p_out.value(1)
    time.sleep(0.3)
    p_out.value(0)
    time.sleep(periode)
    print("Time sleep finished")
