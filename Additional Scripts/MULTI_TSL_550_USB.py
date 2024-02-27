# -*- coding: utf-8 -*-

"""
Created on Mon Sep 27 18:42:37 2021

@maintainer: rakshith
"""

# Basic imports (or dependencies)
import clr
import sys
import time

# Checking and Accessing the DLL (Santec_FTDI) [make sure the DLLs are in the same directory as the script]
assembly_path = r"../DLL"  # device-class path
sys.path.append(assembly_path)
ref = clr.AddReference(r"Santec_FTDI")


# Importing the main method from the DLL as an object ftdi
import Santec_FTDI as ftdi


""" 
Uncomment to know your serial number 
Uncomment below to print all the connected TSLs 
"""
obj = ftdi.FTD2xx_helper()

for i in range(obj.numDevices):
    print("Device Index: {}".format(i))
    print("Type: {}".format(obj.ftdiDeviceList[i].Type))
    print("ID: {:x}".format(obj.ftdiDeviceList[i].ID))
    print("Location ID: {:x}".format(obj.ftdiDeviceList[i].LocId))
    print("Serial Number: {}".format(obj.ftdiDeviceList[i].SerialNumber))
    print("Description: {}".format(obj.ftdiDeviceList[i].Description))
    print("")


""" 
Assuming Two TSLs at the moment, you can create more than two TSL objects 
TSL1 and TSL2 are two objects to two connected TSLs

SERIAL NUMBER: To find the serial of your instrument, first comment all code down here, 
then uncomment the above code and run, then replace the serial number below 
# """
# TSL1 = ftdi.FTD2xx_helper('15070001')       # Replace the with the Instrument Serial Number
# TSL2 = ftdi.FTD2xx_helper('18060001')       # Replace the with the Instrument Serial Number
#
#
# # Devices stores the two objects TSL1 and TSL2
# Devices = [TSL1, TSL2]
#
#
# """
# Loop to perform TSL Sweep one TSL after the other
# Additionally you can add write and query commands for setting various TSL parameters
# """
# for TSL in Devices:
#     # Pre-setting Parameters
#     TSL.Write('SQ')  # Stops any precedent sweep
#     TSL.Write('CF')  # Coherence control off
#     TSL.Write('AF')  # Attenuation auto
#     TSL.Write('SO')  # Opens Internal Shutter
#
#     TSL.Write('TM3')  # Sets trigger output as Step
#     TSL.Write('TRD')  # Disables EXT trigger
#     time.sleep(1)
#
#     TSL.Write('SA0')  # Sets waiting time between 2 sweeps to 0 sec
#     TSL.Write('SZ1')  # Sets repeat cycles to 1 repetition
#
#     TSL.Query('SM7')                      # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep
#     TSL.Query('SO')
#
#     while int(TSL.Query('SK')) != 1:            # Checks the current status of Sweep
#         TSL.Query('SG1')                        # Sets TSL in standby mode (executes only one sweep)
#         time.sleep(1)
#         TSL.Query('ST')                         # Issues Soft trigger
#         break
#
#     print(f'SME Scan in process.............')
#
#     time.sleep(1)
#
#     while int(TSL.Query('SK')) != 0:            # Checks the current status of Sweep
#         time.sleep(1)
#
#     print('----- Sweep Done -----')
#
#
# # Outputs the Wavelength list
# Data1 = [i/10000 for i in TSL1.GetAllDataPointsFromLastScan_SantecCommand()]          # Reads logg wavelengths
# Data2 = [i/10000 for i in TSL2.GetAllDataPointsFromLastScan_SantecCommand()]          # Reads logg wavelengths
# print('\nWavelength data of TSL1: \n', Data1)
# print('\nWavelength data of TSL2: \n', Data2)
