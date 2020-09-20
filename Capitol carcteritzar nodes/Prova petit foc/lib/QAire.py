from machine import ADC
import machine
import time

N=100
#Use the typical sensitivity in units of V per 100ug/m3.
K = 0.58

class QAire:
    sharpVoPin='P20'  #G7
    sharpLEDPin='P21' #G8

    def __init__(self,apin,dpin):
        self.sharpVoPin=apin
        self.sharpLEDPin=dpin

        self.dac = machine.DAC(self.sharpLEDPin)   # create a DAC object on pin P20 G7
        self.adc = machine.ADC()             # create an ADC object
        self.apin = self.adc.channel(pin=self.sharpVoPin,attn=ADC.ATTN_11DB)   # create an analog pin on P21 G8
        VoRawTotal=0
        self.Vo=0
        self.dV=0
        #Set the typical output voltage in Volts when there is zero dust.
        self.Voc=100 #mV

        # for i in range(N):
        #     self.dac.write(0)                          # set output to 0% = GND. Power ON the LED
        #
        #     time.sleep(0.000280)
        #
        #     self.VoRaw = self.apin.voltage()              # read an analog value voltage in mV
        #
        #     self.dac.write(1)                          # set output to 100% = 3.3V. Power OFF the LED
        #
        #     #Wait for remainder of the 10ms cycle = 10000 - 280 - 100 microseconds.
        #     time.sleep(0.009620)
        #
        #     VoRawTotal=VoRawTotal+self.VoRaw
        #
        # #Averaging of the voltage read:
        # Vo=VoRawTotal/N
        # VoRawTotal=0
        #
        # # Convert to Dust Density in units of ug/m3.
        # self.dV = self.Vo - self.Voc
        # if ( self.dV < 0 ):
        #   self.dV = 0
        #   self.Voc = self.Vo
        # print("Voc",self.Voc,"mV")

    def CalculateDust(self):
        self.dac.write(0)                          # set output to 0% = GND

        time.sleep(0.000280)

        self.VoRaw = self.apin.voltage()              # read an analog value voltage in mV
        #print("read: ",self.apin())
        self.dac.write(1)                          # set output to 100% = 3.3V

        #Wait for remainder of the 10ms cycle = 10000 - 280 - 100 microseconds.
        time.sleep(0.009620)

        # Convert to Dust Density in units of ug/m3.
        self.dV = self.VoRaw - self.Voc
        if ( self.dV < 0 ):
          self.dV = 0

        print("Vo",self.VoRaw,"mV")

        dustDensity = self.dV*0.001 / (K/100)

        return(dustDensity)



# digitalWrite(sharpLEDPin, LOW);
#
#   // Wait 0.28ms before taking a reading of the output voltage as per spec.
#   delayMicroseconds(280);
#
#   // Record the output voltage. This operation takes around 100 microseconds.
#   int VoRaw = analogRead(sharpVoPin);
#
#   // Turn the dust sensor LED off by setting digital pin HIGH.
#   digitalWrite(sharpLEDPin, HIGH);

#   // Wait for remainder of the 10ms cycle = 10000 - 280 - 100 microseconds.
# delayMicroseconds(9620);

# // Use averaging if needed.
#   float Vo = VoRaw;
#   #ifdef USE_AVG
#   VoRawTotal += VoRaw;
#   VoRawCount++;
#   if ( VoRawCount >= N ) {
#     Vo = 1.0 * VoRawTotal / N;
#     VoRawCount = 0;
#     VoRawTotal = 0;
#   } else {
#     return;
#   }
#   #endif // USE_AVG

#   // Compute the output voltage in Volts.
#   Vo = Vo / 1024.0 * 5.0;
#   printFValue("Vo", Vo*1000.0, "mV");
#
#   // Convert to Dust Density in units of ug/m3.
#   float dV = Vo - Voc;
#   if ( dV < 0 ) {
#     dV = 0;
#     Voc = Vo;
#   }
#   float dustDensity = dV / K * 100.0;
#   printFValue("DustDensity", dustDensity, "ug/m3", true);
# Serial.println("");
