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
#     TSL.Write('POW:UNIT 0')  # Sets power unit to dBm
#     TSL.Write('WAV:UNIT 0')  # Sets lambda units to nm
#     TSL.Write('COHCtrl 0')  # Coherence control off
#     TSL.Write('POW:ATT:AUT 1')  # Attenuation auto
#     TSL.Write('POW:ATT 0')
#     TSL.Write('AM:STAT 0')  # Disables amplitude Modulation
#     TSL.Write('PW:SHUT 0')  # Opens Internal Shutter
#     TSL.Write('WAV:SWE 0')
#
#     TSL.Write('TRIG:OUTP 3')  # Set trigger output as Step
#     TSL.Write('TRIG:INP:EXT 0')  # Disable EXT trigger
#
#     opc = 0
#     while opc == 0:
#         opc = TSL.Query('*OPC?')
#     TSL.Write('TRIG:INP:STAN 1')  # Sets TSL in standby mode (executes only one sweep)
#     TSL.Write('WAV:SWE 1')  # TSL Sweep Status to start
#     opc = 0
#     time.sleep(0.5)
#     while opc == 0:
#         opc = TSL.Query('*OPC?')
#     check2 = TSL.Query('WAV:SWE?')
#
#     while check2 != '3':
#         check2 = TSL.Query('WAV:SWE?')
#         time.sleep(0.1)
#     TSL.Write('WAV:SWE:SOFT')  # Issues Soft Trigger
#
#     print('\nScan started....')
#
#     opc = int(TSL.Query('WAV:SWE?'))
#     while opc != 0:
#         time.sleep(0.05)
#         opc = int(TSL.Query('WAV:SWE?'))
#
#     print('\nScan done...')
#
#
# # Outputs the Wavelength list
# Data1 = [i/10000 for i in TSL1.GetAllDataPointsFromLastScan_SantecCommand()]          # Reads logg wavelengths
# Data2 = [i/10000 for i in TSL2.GetAllDataPointsFromLastScan_SantecCommand()]          # Reads logg wavelengths
# print('\nWavelength data of TSL1: \n', Data1)
# print('\nWavelength data of TSL2: \n', Data2)
