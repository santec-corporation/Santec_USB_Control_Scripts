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
    TSL1.Write('SQ')  # Stops any precedent sweep
    TSL1.Write('CF')  # Coherence control off
    TSL1.Write('AF')  # Attenuation auto
    TSL1.Write('SO')  # Opens Internal Shutter

    TSL1.Write('TM3')  # Sets trigger output as Step
    TSL1.Write('TRD')  # Disables EXT trigger
    time.sleep(1)

    TSL1.Write('SA0')  # Sets waiting time between 2 sweeps to 0 sec
    TSL1.Write('SZ1')  # Sets repeat cycles to 1 repetition

    TSL1.Query('SM7')  # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep
    TSL1.Query('SO')

    while int(TSL1.Query('SK')) != 1:  # Checks the current status of Sweep
        TSL1.Query('SG1')  # Sets TSL1 in standby mode (executes only one sweep)
        time.sleep(1)
        TSL1.Query('ST')  # Issues Soft trigger
        break

    print('TSL1 Scan in process.............')

    time.sleep(1)

    while int(TSL1.Query('SK')) != 0:  # Checks the current status of Sweep
        time.sleep(1)

    print('----- TSL1 Sweep Done -----')


def instrument_2_function():
    TSL2.Write('SQ')  # Stops any precedent sweep
    TSL2.Write('CF')  # Coherence control off
    TSL2.Write('AF')  # Attenuation auto
    TSL2.Write('SO')  # Opens Internal Shutter

    TSL2.Write('TM3')  # Sets trigger output as Step
    TSL2.Write('TRD')  # Disables EXT trigger
    time.sleep(1)

    TSL2.Write('SA0')  # Sets waiting time between 2 sweeps to 0 sec
    TSL2.Write('SZ1')  # Sets repeat cycles to 1 repetition

    TSL2.Query('SM7')  # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep
    TSL2.Query('SO')

    while int(TSL2.Query('SK')) != 1:  # Checks the current status of Sweep
        TSL2.Query('SG1')  # Sets TSL2 in standby mode (executes only one sweep)
        time.sleep(1)
        TSL2.Query('ST')  # Issues Soft trigger
        break

    print('TSL2 Scan in process.............')

    time.sleep(1)

    while int(TSL2.Query('SK')) != 0:  # Checks the current status of Sweep
        time.sleep(1)

    print('----- TSL2 Sweep Done -----')


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
