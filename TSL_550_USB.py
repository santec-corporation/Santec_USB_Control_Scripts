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
TSL.Write('*CLS')                                                               # Clears all status
TSL.Write('*RST')                                                               # Resets all status
TSL.Write('GC 0')                                                               # Sets TSL to santec command system
TSL.Write('GD2')                                                                # Select CF+LF GPIB delimiter


# Checks if TSL Laser Diode (LD) is ON, else switches it ON
check0 = TSL.Query('SU')[0]             # Checks if LD is ON
if check0 == '-' or 'N':
    pass
else:
    TSL.Write('LO')                                                             # Sets LD ON
    print('LD switching ON, please wait')
    while TSL.Query('SU')[0] != '-':
        time.sleep(1)
        pass
    print('LD is ON now')

# Pre-setting Parameters
TSL.Write('SQ')                                                                 # Stops any precedent sweep
TSL.Write('CF')                                                                 # Coherence control off
TSL.Write('AF')                                                                 # Attenuation auto
TSL.Write('SO')                                                                 # Opens Internal Shutter

TSL.Write('TM3')                                                                # Sets trigger output as Step
TSL.Write('TRD')                                                                # Disables EXT trigger
time.sleep(1)


# Input parameters
print('Input output power: ')
pwr = input()
TSL.Write('OP'+pwr)

TSL.Write('SM7')                          # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep
time.sleep(0.5)

print('Input start wavelength: ')
WLS = input()
TSL.Write('SS'+WLS)
TSL.Write('WA'+WLS)

print('Input end wavelength: ')
WLE = input()
TSL.Write('SE'+WLE)
time.sleep(0.5)

print('Input scan speed:')
speed = input()
TSL.Write('SN'+speed)
time.sleep(0.5)

TSL.Write('SA0')                                                           # Sets waiting time between 2 sweeps to 0 sec
TSL.Write('SZ1')                                                                # Sets repeat cycles to 1 repetition

print('Input Step (pm)')
Step = str(float(input())/1000)
TSL.Write('TW'+Step)
time.sleep(0.5)

# Sweep Logic
TSL.Write('SG1')                                                    # Sets TSL in standby mode (executes only one sweep)
su = 1
while su != 0:
    su = int(TSL.Query('SU')[6])

print('Press any key to start the scan')
input()
TSL.Write('ST')                                                                    # Issues Soft trigger

while bytes(TSL.Query('SK'), 'utf8') != b'000000':                                 # Checks if TSL is busy
    time.sleep(0.1)


# Outputs the Wavelength list
raw = [i/10000 for i in TSL.GetAllDataPointsFromLastScan_SantecCommand()]          # Reads logg wavelengths
print(raw)
