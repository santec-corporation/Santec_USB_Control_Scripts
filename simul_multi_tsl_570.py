# -*- coding: utf-8 -*-

"""
Created on Mon Sep 27 18:42:37 2021

@maintainer: rakshith
"""

# Basic imports (or dependencies)
import clr
import sys
import time
import threading


# Checking and Accessing the DLL (Santec_FTDI) [make sure the DLLs are in the same directory as the script]
assembly_path = r"../DLL"  # device-class path
sys.path.append(assembly_path)
ref = clr.AddReference(r"Santec_FTDI")


# Importing the main method from the DLL as an object ftdi
import Santec_FTDI as ftdi


""" 
Uncomment to know your serial number 
Uncomment below to print all the connected TSL1s 
"""
# obj = ftdi.FTD2xx_helper()
#
# for i in range(obj.numDevices):
#     print("Device Index: {}".format(i))
#     print("Type: {}".format(obj.ftdiDeviceList[i].Type))
#     print("ID: {:x}".format(obj.ftdiDeviceList[i].ID))
#     print("Location ID: {:x}".format(obj.ftdiDeviceList[i].LocId))
#     print("Serial Number: {}".format(obj.ftdiDeviceList[i].SerialNumber))
#     print("Description: {}".format(obj.ftdiDeviceList[i].Description))
#     print("")


""" 
Assuming Two TSL1s at the moment, you can create more than two TSL1 objects 
TSL11 and TSL12 are two objects to two connected TSL1s

SERIAL NUMBER: To find the serial of your instrument, first comment all code down here, 
then uncomment the above code and run, then replace the serial number below 
"""
TSL1 = ftdi.FTD2xx_helper('15070001')  # Replace the with the Instrument Serial Number
TSL2 = ftdi.FTD2xx_helper('18060001')  # Replace the with the Instrument Serial Number


# Devices stores the two objects TSL11 and TSL12
def instrument_1_function():
    # Pre-setting Parameters
    TSL1.Write('POW:UNIT 0')  # Sets power unit to dBm
    TSL1.Write('WAV:UNIT 0')  # Sets lambda units to nm
    TSL1.Write('COHCtrl 0')  # Coherence control off
    TSL1.Write('POW:ATT:AUT 1')  # Attenuation auto
    TSL1.Write('POW:ATT 0')
    TSL1.Write('AM:STAT 0')  # Disables amplitude Modulation
    TSL1.Write('PW:SHUT 0')  # Opens Internal Shutter
    TSL1.Write('WAV:SWE 0')

    TSL1.Write('TRIG:OUTP 3')  # Set trigger output as Step
    TSL1.Write('TRIG:INP:EXT 0')  # Disable EXT trigger

    opc = 0
    while opc == 0:
        opc = TSL1.Query('*OPC?')
    TSL1.Write('TRIG:INP:STAN 1')  # Sets TSL in standby mode (executes only one sweep)
    TSL1.Write('WAV:SWE 1')  # TSL Sweep Status to start
    opc = 0
    time.sleep(0.5)
    while opc == 0:
        opc = TSL1.Query('*OPC?')
    check2 = TSL1.Query('WAV:SWE?')

    while check2 != '3':
        check2 = TSL1.Query('WAV:SWE?')
        time.sleep(0.1)
    TSL1.Write('WAV:SWE:SOFT')  # Issues Soft Trigger

    print('\nScan started....')

    opc = int(TSL1.Query('WAV:SWE?'))
    while opc != 0:
        time.sleep(0.05)
        opc = int(TSL1.Query('WAV:SWE?'))

    print('\nScan done...')


def instrument_2_function():
    # Pre-setting Parameters
    TSL2.Write('POW:UNIT 0')  # Sets power unit to dBm
    TSL2.Write('WAV:UNIT 0')  # Sets lambda units to nm
    TSL2.Write('COHCtrl 0')  # Coherence control off
    TSL2.Write('POW:ATT:AUT 1')  # Attenuation auto
    TSL2.Write('POW:ATT 0')
    TSL2.Write('AM:STAT 0')  # Disables amplitude Modulation
    TSL2.Write('PW:SHUT 0')  # Opens Internal Shutter
    TSL2.Write('WAV:SWE 0')

    TSL2.Write('TRIG:OUTP 3')  # Set trigger output as Step
    TSL2.Write('TRIG:INP:EXT 0')  # Disable EXT trigger

    opc = 0
    while opc == 0:
        opc = TSL2.Query('*OPC?')
    TSL2.Write('TRIG:INP:STAN 1')  # Sets TSL in standby mode (executes only one sweep)
    TSL2.Write('WAV:SWE 1')  # TSL Sweep Status to start
    opc = 0
    time.sleep(0.5)
    while opc == 0:
        opc = TSL2.Query('*OPC?')
    check2 = TSL2.Query('WAV:SWE?')

    while check2 != '3':
        check2 = TSL2.Query('WAV:SWE?')
        time.sleep(0.1)
    TSL2.Write('WAV:SWE:SOFT')  # Issues Soft Trigger

    print('\nScan started....')

    opc = int(TSL2.Query('WAV:SWE?'))
    while opc != 0:
        time.sleep(0.05)
        opc = int(TSL2.Query('WAV:SWE?'))

    print('\nScan done...')


# Create threads for each instrument
thread_1 = threading.Thread(target=instrument_1_function)
thread_2 = threading.Thread(target=instrument_2_function)

# Start the threads
thread_1.start()
thread_2.start()

# Wait for both threads to finish
thread_1.join()
thread_2.join()


# Outputs the Wavelength list (Uncomment below to print wavelength data)
# Data1 = [i / 10000 for i in TSL1.GetAllDataPointsFromLastScan_SantecCommand()]  # Reads logg wavelengths
# time.sleep(1)
# Data2 = [i / 10000 for i in TSL2.GetAllDataPointsFromLastScan_SantecCommand()]  # Reads logg wavelengths
# time.sleep(1)
# print('\nWavelength data of TSL1: \n', Data1)
# print('\nWavelength data of TSL2: \n', Data2)
