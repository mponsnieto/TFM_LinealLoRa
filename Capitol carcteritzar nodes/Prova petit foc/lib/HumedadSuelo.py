import machine
class HumitatSol:
    def __init__(self,pin):
        self.p=pin
        pass
    def CalcularHumitat(self):
        adc = machine.ADC()             # create an ADC object
        apin = adc.channel(pin=self.p)   # create an analog pin on P16
        val = apin()                    # read an analog value

        dry=False
        humid=False
        inWater=False
        if val <300:
            dry=True
        elif val< 700:
            humid=True
        else:
            inWater=True
        return(val,dry,humid,inWater)

    def saveFile(self,dhi,val,rtc):
            '''
            Format of the data: date (DD/MM/YYYY HH:MM:SS) Temperature [ºC]
            Example: 15/10/2019 13:21:31 26.4
            '''
            #Write the image temp in data.txt
            f = open('data_Hsuelo.txt', 'a')
            f.write("{}/{}/{} {}:{}:{} dhi {} val {}\n".format(rtc.now()[2],rtc.now()[1],rtc.now()[0],rtc.now()[3],rtc.now()[4],rtc.now()[5],dhi,val))
            f.close()
            return
