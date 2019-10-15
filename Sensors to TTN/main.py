com.JoinLoraWan()
periode=120  #2min
print("Start")
while True:
    #Sensor PT BMP085
    temp = bmp.GetTemperature
    packet_tbmp= ustruct.pack('H',int(temp))
    # packet_tbmp = ustruct.pack('f',temp)
    # dataBMP="Temp: %0.2f *C" % (temp)
    # print(dataBMP)
    bmp.saveFile(temp)
    time.sleep(0.3)

    # #Sensor T MCP
    tempC = mcp.GetTemperature
    packet_tempC= ustruct.pack('H',int(tempC))
    #packet_tempC = ustruct.pack('f',tempC)
    #dataMCP='Temperature: {} C '.format(tempC)
    #print(dataMCP)
    time.sleep(0.3)

    #Sensor HS
    val,dry,humid,inWater=sensorHSol.CalcularHumitat()
    dhi=dry+humid*2+inWater*3
    packet_val= ustruct.pack('H',int(val))
    packet_dhi= ustruct.pack('B',int(dhi))
    time.sleep(0.3)

    #Sensor QAire
    dustDensity=sensorQAire.CalculateDust()
    time.sleep(0.3)
    #print("DustDensity: ",dustDensity," ug/m3")
    packet_dust= ustruct.pack('H',int(dustDensity))

    #Càmera
    Temp=cam.readTemp
    packet_T_cam= ustruct.pack('H',int(Temp))
    # print("T from thermistor= %0.2f *C" % (Temp))
    T=cam.readPixels
    # print("Image readen pixel by pixel in *C")
    # for i in range(8): print(T[i])
    time.sleep(0.3)

    #Sensor HT
    T=SensorHT.readTemperature()
    time.sleep(0.3)
    H=SensorHT.readHumidity()
    time.sleep(0.3)
    packet_Tht= ustruct.pack('H',int(T))
    packet_Hht= ustruct.pack('B',round(int(H)))

    # com.EnviarGateway(dataHS)
    # com.EnviarGateway(dataBMP)
    # com.EnviarGateway(dataMCP)
    # com.EnviarGateway(str(dustDensity))
    # com.EnviarGateway(str(T))
    # com.EnviarGateway(str(H))
    print("Sending to GTW...")
    com.EnviarGateway(packet_dust+packet_tempC+packet_Tht+packet_Hht+packet_tbmp+packet_val+packet_dhi+packet_T_cam+id_aux)
    time.sleep(periode)
    print("Time sleep finished")
