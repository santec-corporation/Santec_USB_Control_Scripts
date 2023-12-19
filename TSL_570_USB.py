# -*- coding: utf-8 -*-

"""
Created on Mon Sep 27 18:42:37 2021

@author: chentir
"""

# Basic imports (or dependencies)
import clr
import sys
import time

# Checking and Accessing the DLL (Santec_FTDI) [make sure the DLLs are in the same directory as the script]
assembly_path = r".\DLL"                                                # device-class path
sys.path.append(assembly_path)
ref = clr.AddReference(r"Santec_FTDI")


# Importing the main method from the DLL
import Santec_FTDI as ftdi


# Object to method to control the instrument
TSL = ftdi.FTD2xx_helper()                 # you can also pass the instrument serial number as parameter of a specific device


# Basic commands
TSL.Write('*CLS')
TSL.Write('*RST')
TSL.Write('SYST:COMM:GPIB:DEL 2')       # Select CF+LF GPIB delimiter
TSL.Write('SYST:COMM:COD 0')            # Set communication into LEGACY command
TSL.Write('TRIG:OUTP:SETT 0')      # Sets the output trigger to be periodic in wavelength. Arg= 1 to set the trigger to be periodic in time


# Checks if TSL Laser Diode (LD) is ON
check0 = TSL.Query('POW:STAT?')
print(check0)
if check0 == '0':
    TSL.Write('POW:STAT 1')             # Sets LD ON
    print('LD switching ON, please wait')
    while True:
        if int(TSL.Query('POW:STAT?')) == 0:
            time.sleep(10)
        else:
            print('LD is ON now')
            break
else:
    pass


# Pre-setting Parameters
TSL.Write('POW:UNIT 0')              # Sets power unit to dBm
TSL.Write('WAV:UNIT 0')              # Sets lambda units to nm
TSL.Write('COHCtrl 0')               # Coherence control off
TSL.Write('POW:ATT:AUT 1')          # Attenuation auto
TSL.Write('POW:ATT 0')
TSL.Write('AM:STAT 0')              # Disables amplitude Modulation
TSL.Write('PW:SHUT 0')              # Opens Internal Shutter
TSL.Write('WAV:SWE 0')

TSL.Write('TRIG:OUTP 3')            # Set trigger output as Step
TSL.Write('TRIG:INP:EXT 0')         # Disable EXT trigger


# Input parameters
print('Input output power')
PWR = input()
TSL.Write(f'POW {PWR}')

TSL.Write('WAV:SWE:MOD 1')                # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep

print('Input start wavelength:')
WLS = input()
TSL.Write('WAV:SWE:STAR '+WLS)
TSL.Write('WAV '+WLS)
print('Input end wavelength:')
WLE = input()
TSL.Write('WAV:SWE:STOP '+WLE)

print('Input scan speed:')
speed = input()
TSL.Write('WAV:SWE:SPE '+speed)

TSL.Write('WAV:SWE:DEL 0')
TSL.Write('WAV:SWE:CYCL 1')             # Sets repeat cycles to 1 repetition

print('Input Step (pm)')
Step = str(float(input())/1000)
TSL.Write('TRIG:OUTP:STEP '+Step)

TSL.Write('WAV '+WLS)
opc = 0
while opc == 0:
    opc = TSL.Query('*OPC?')
TSL.Write('TRIG:INP:STAN 1')            # Sets TSL in standby mode (executes only one sweep)
TSL.Write('WAV:SWE 1')                  # TSL Sweep Status to start
opc = 0
time.sleep(0.5)
while opc == 0:
    opc = TSL.Query('*OPC?')
check2 = TSL.Query('WAV:SWE?')

while check2 != '3':
    check2 = TSL.Query('WAV:SWE?')
    time.sleep(0.1)
TSL.Write('WAV:SWE:SOFT')                   # Issues Soft Trigger


opc = 0
while opc == 0:                             # Checks if TSL is busy
    opc = TSL.Query('*OPC?')
    break


# Outputs the Wavelength list
raw = [i / 10000 for i in TSL.GetAllDataPointsFromLastScan_SCPICommand()]       # Read LOG data
round_off = [round(num, 1) for num in raw]
print(round_off)
