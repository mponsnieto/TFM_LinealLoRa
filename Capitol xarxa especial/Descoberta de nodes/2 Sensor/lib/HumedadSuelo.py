import machine

class HumitatSol:
    def __init__(self):
        pass
    def CalcularHumitat(self):

        
        adc = machine.ADC()             # create an ADC object
        apin = adc.channel(pin='P19',attn=machine.ADC.ATTN_11DB)   # create an analog pin on P16
        val = apin()                    # read an analog value
        volt=apin.voltage()
        print("Voltatge = ")
        print(volt)
        print(val)
        per= 0.0534*volt - 7.5855
        print("percentatge: ", per)
        dry=False
        humid=False
        inWater=False
        if per <30:
            dry=True
        elif per< 70:
            humid=True
        else:
            inWater=True
        return(val,dry,humid,inWater)
