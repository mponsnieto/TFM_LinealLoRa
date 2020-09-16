
periode=0.5*60  #2min
print("Start")
while True:
    #sensor sensorQAire
    #sensorAmphenol.readDust()

    #Sensor PT BMP085
    temp = bmp.GetTemperature
    dataBMP="Temp BMP: %0.2f *C" % (temp)
    print(dataBMP)
    bmp.saveFile(temp,rtc)
    time.sleep(0.3)

    # #Sensor T MCP
    tempC = mcp.GetTemperature
    dataMCP='Temp MCP: {} C '.format(tempC)
    print(dataMCP)
    mcp.saveFile(tempC,rtc)
    time.sleep(0.3)

    #Sensor HS
    val,dry,humid,inWater=sensorHSol.CalcularHumitat()
    dhi=dry+humid*2+inWater*3
    print("Hsuelo: dhi",dhi," val ",val)
    sensorHSol.saveFile(dhi,val,rtc)
    time.sleep(0.3)


    #Sensor QAire/ Particules
    pm1, pm25,pm10 = pma.read_particules()
    dustDensity=sensorQAire.CalculateDust()
    # packet_dust= ustruct.pack('H',int(dustDensity))
    #packet_dust= ustruct.pack('H',int(pm10))
    print("DustDensity Amphenol: ",pm25," ug/m3")
    #saveFileParticulas(rtc,pm25,pm10,dustDensity)
    time.sleep(0.3)
    #Sensor QAire
    dustDensity=sensorQAire.CalculateDust()
    time.sleep(0.3)
    print("DustDensity: ",dustDensity," ug/m3")

    #Càmera
    Temp=cam.readTemp
    print("T from thermistor= %0.2f *C" % (Temp))
    T=cam.readPixels
    print("Image readen pixel by pixel in *C")
    for i in range(8): print(T[i])
    cam.saveFile(T,Temp,rtc)
    time.sleep(0.3)

    #Sensor HT
    T=SensorHT.readTemperature()
    SensorHT.saveFile(T,rtc)
    time.sleep(0.3)
    H=SensorHT.readHumidity()
    time.sleep(0.3)

    #Waiting time
    time.sleep(periode)
    print("Time sleep finished")
