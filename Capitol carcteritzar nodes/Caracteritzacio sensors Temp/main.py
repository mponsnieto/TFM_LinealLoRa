periode=5*60  #min
print("Start")
while True:
    #Sensor PT BMP085
    temp = bmp.GetTemperature
    packet_tbmp= ustruct.pack('H',int(temp))
    # packet_tbmp = ustruct.pack('f',temp)
    # dataBMP="Temp: %0.2f *C" % (temp)
    # print(dataBMP)
    bmp.saveFile(temp,rtc)
    time.sleep(0.3)

    # #Sensor T MCP
    tempC = mcp.GetTemperature
    packet_tempC= ustruct.pack('H',int(tempC))
    #packet_tempC = ustruct.pack('f',tempC)
    #dataMCP='Temperature: {} C '.format(tempC)
    #print(dataMCP)
    mcp.saveFile(tempC,rtc)
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
    cam.saveFile(T,Temp,rtc)
    time.sleep(0.3)

    #Sensor HT
    T=SensorHT.readTemperature()
    SensorHT.saveFile(T,rtc)
    time.sleep(0.3)
    H=SensorHT.readHumidity()
    time.sleep(0.3)
    packet_Tht= ustruct.pack('H',int(T))
    packet_Hht= ustruct.pack('B',round(int(H)))

    print("All sensors data saved...")
    time.sleep(periode)
    print("Time sleep finished")
