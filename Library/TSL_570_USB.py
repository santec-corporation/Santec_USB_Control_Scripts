# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 18:42:37 2021

@author: chentir
"""

import time
import clr
import sys

assembly_path = r".\DLL"                                                #dll path
sys.path.append(assembly_path)
ref = clr.AddReference(r"Santec_FTDI")

from Santec_FTDI import FTD2xx_helper


TSL = FTD2xx_helper()
raw = []

TSL.Write('*CLS')
TSL.Write('*RST')
TSL.Write('SYST:COMM:GPIB:DEL 2')                                              #Select CF+LF GPIB delimiter
TSL.Write('SYST:COMM:COD 0')                                                   #Set communication into LEGACY command
TSL.Write('TRIG:OUTP:SETT 0')                                                  #Sets the output trigger to be periodic in wavelength. Arg= 1 to set the trigger to be periodic in time
check0=TSL.Query('POW:STAT?')                                                  
if check0=='0':
    TSL.Write('POW:STAT 1')                                                    #Sets LD ON
    print ('LD switching ON, please wait')
    while True:
        if int(TSL.Query('POW:STAT?'))==0:
            time.sleep(10)
        else:
            print('LD is ON now')
            break
else:
    pass

TSL.Write('POW:UNIT 0')                                                        #Sets power unit to dBm
TSL.Write('WAV:UNIT 0')                                                        #Sets lambda units to nm
TSL.Write('COHCtrl 0')                                                         #Coherence control off
TSL.Write('POW:ATT:AUT 1')                                                     #Attenuation auto
TSL.Write('POW:ATT 0')
TSL.Write('AM:STAT 0')                                                         #Disables amplitude Modulation
TSL.Write('PW:SHUT 0')                                                         #Opens Internal Shutter
TSL.Write('WAV:SWE 0')

TSL.Write('TRIG:OUTP 3')                                                       #Set trigger output as Step
TSL.Write('TRIG:INP:EXT 0')                                                    #Disable EXT trigger

print('Input output power')
PWR = input()
TSL.Write(f'POW {PWR}')

TSL.Write('WAV:SWE:MOD 1')


print('Input start wavelength:')
WLS=input()
TSL.Write('WAV:SWE:STAR '+WLS)
TSL.Write('WAV '+WLS)
print('Input end wavelength:')
WLE=input()
TSL.Write('WAV:SWE:STOP '+WLE)

print('Input scan speed:')
speed=input()
TSL.Write('WAV:SWE:SPE '+speed)

TSL.Write('WAV:SWE:DEL 0')
TSL.Write('WAV:SWE:CYCL 1')

print('Input Step (pm)')
Step = str(float(input())/1000)
TSL.Write('TRIG:OUTP:STEP '+Step)

TSL.Write('WAV '+WLS)
opc = 0
while opc  == 0:
    opc = TSL.Query('*OPC?')
TSL.Write('TRIG:INP:STAN 1')
TSL.Write('WAV:SWE 1')
opc = 0
time.sleep(0.5)
while opc  == 0:
    opc = TSL.Query('*OPC?')
check2=TSL.Query('WAV:SWE?')

while check2 != '3':
    check2=TSL.Query('WAV:SWE?')
    time.sleep(0.1)
TSL.Write('WAV:SWE:SOFT')
opc = 0
while opc  == 0:
    opc = TSL.Query('*OPC?')
    break

raw = [i/10000 for i in TSL.GetAllDataPointsFromLastScan_SCPICommand()]        #Read LOG data
