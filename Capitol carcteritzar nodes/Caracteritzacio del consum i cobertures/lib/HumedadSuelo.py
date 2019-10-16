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
