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

# Checking for Santec instruments and selecting a TSL
ftdi_class = ftdi.FTD2xx_helper

list_of_devices = ftdi_class.ListDevices()

tslDevice_list = []

for device in list_of_devices:
    if 'TSL' in device.Description:
        tslDevice_list.append(device)

for tsl in range(len(tslDevice_list)):
    print(f'TSL number: {tsl+1}, Name: {tslDevice_list[tsl].Description}, Serial Number: {tslDevice_list[tsl].SerialNumber}')

TSL = None

if tslDevice_list:
    user_select = int(input('\nEnter the TSL number to control')) - 1

    user_select_tsl_serial = tslDevice_list[user_select].SerialNumber
    TSL = ftdi.FTD2xx_helper(user_select_tsl_serial)

print(f'\nSelected TSL Device: {TSL.QueryIdn()}')


# Basic commands
TSL.Write('*CLS')                                                               # Clears all status
TSL.Write('*RST')                                                               # Resets all status
TSL.Write('GC 0')                                                               # Sets TSL to santec command system
TSL.Write('GD2')                                                                # Select CF+LF GPIB delimiter


# Checks if TSL Laser Diode (LD) is ON
check0 = TSL.Query('SU')[0]             # Checks if LD is ON
print(check0)
if check0 != '-':
    TSL.Write('LO')  # Sets LD ON
    print('\nLD switching ON, please wait')
    while TSL.Query('SU')[0] != '-':
        time.sleep(1)
        pass
    print('\nLD is ON now')
else:
    pass


# Pre-setting Parameters
TSL.Write('SQ')                                                                 # Stops any precedent sweep
TSL.Write('CF')                                                                 # Coherence control off
TSL.Write('AF')                                                                 # Attenuation auto
TSL.Write('SO')                                                                 # Opens Internal Shutter

TSL.Write('TM3')                                                                # Sets trigger output as Step
TSL.Write('TRD')                                                                # Disables EXT trigger
time.sleep(1)


# Input parameters
print('\nInput output power: ')
pwr = input()
TSL.Write('OP'+pwr)

TSL.Write('SM7')                          # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep
time.sleep(0.5)

print('\nInput start wavelength: ')
WLS = input()
TSL.Write('SS'+WLS)
TSL.Write('WA'+WLS)

print('\nInput end wavelength: ')
WLE = input()
TSL.Write('SE'+WLE)
time.sleep(0.5)

print('\nInput scan speed:')
speed = input()
TSL.Write('SN'+speed)
time.sleep(0.5)

TSL.Write('SA0')                                                           # Sets waiting time between 2 sweeps to 0 sec
TSL.Write('SZ1')                                                                # Sets repeat cycles to 1 repetition

print('\nInput Step (pm)')
Step = str(float(input())/1000)
TSL.Write('TW'+Step)
time.sleep(0.5)

# Sweep Logic
TSL.Write('SG1')                                                    # Sets TSL in standby mode (executes only one sweep)
su = 1
while su != 0:
    su = int(TSL.Query('SU')[6])

print('\nPress any key to start the scan')
input()
TSL.Write('ST')                                                                    # Issues Soft trigger

while bytes(TSL.Query('SK'), 'utf8') != b'000000':                                 # Checks if TSL is busy
    time.sleep(0.1)


# Outputs the Wavelength list
raw = [i/10000 for i in TSL.GetAllDataPointsFromLastScan_SantecCommand()]          # Reads logg wavelengths
print(raw)
