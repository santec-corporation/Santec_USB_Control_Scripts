# -*- coding: utf-8 -*-

"""
Santec TSL 570 USB Script
Updated on Tues May 21 13:00:00 2024

@organization: santec holdings corp.
"""

# Basic imports (or dependencies)
import clr
import sys
import time
import logger

# Checking and Accessing the DLL (Santec_FTDI) [make sure the DLLs are in the same directory as the script]
assembly_path = r".\DLL"  # device-class path
sys.path.append(assembly_path)
ref = clr.AddReference(r"Santec_FTDI")
# print(ref)

# Importing the helper class from Santec_FTDI DLL
import Santec_FTDI as ftdi
ftdi_helper = ftdi.FTD2xx_helper

list_of_devices = ftdi_helper.ListDevices()
# print(list_of_devices[0].Description)

tslDevice_list = []


class TSL570:
    def __init__(self):
        self.tsl_device_list = []
        self.TSL = None
        self.GetDevices()

    def GetDevices(self):
        log.Info("GetDevices method")
        for device in list_of_devices:
            log.Info("Getting TSL devices from list_of_devices")
            if not 'TSL' in device.Description:
                log.Warning(f"No TSL devices found.")
                raise RuntimeError("Please connect a TSL and restart the program.")
            self.tsl_device_list.append(device)

        for tsl in range(len(self.tsl_device_list)):
            print(f'TSL number: {tsl + 1} | '
                  f'Name: {self.tsl_device_list[tsl].Description} | '
                  f'Serial Number: {self.tsl_device_list[tsl].SerialNumber}')

        if self.tsl_device_list:
            log.Info("User TSL device selection")
            user_select_tsl = int(input('\nEnter the TSL number to control: ')) - 1
            if not isinstance(user_select_tsl, int):
                log.Warning(f"Invalid input type: {type(user_select_tsl)}. Expected int.")
                raise ValueError("Input must be an integer")

            log.Info("Connecting to selected TSL")
            user_select_tsl_serial = self.tsl_device_list[user_select_tsl].SerialNumber
            self.TSL = ftdi.FTD2xx_helper(user_select_tsl_serial)
            if self.TSL is None:
                log.Info(f"Could not connect to TSL device")
                raise RuntimeError("Could not connect to TSL device. Reconnect the TSL to your PC.")

        print(f'\nSelected TSL Device: {self.TSL.QueryIdn()}')
        log.Info(f"TSL Successfully connected {self.TSL.QueryIdn()}")


    def DeviceOperations(self):
        """ Basic TSL 570 operations """
        log.Info("Device Operations")

        " Basic commands "
        self.TSL.Write('*CLS')
        self.TSL.Write('*RST')
        self.TSL.Write('SYST:COMM:GPIB:DEL 2')      # Select CF+LF GPIB delimiter
        self.TSL.Write('SYST:COMM:COD 0')           # Set communication into LEGACY command
        self.TSL.Write('TRIG:OUTP:SETT 0')          # Sets the output trigger to be periodic in wavelength. Arg= 1 to set the trigger to be periodic in time

        " Checks if TSL Laser Diode (LD) is ON "
        check0 = self.TSL.Query('POW:STAT?')
        # print(check0)

        if check0 == '0':
            self.TSL.Write('POW:STAT 1')  # Sets LD ON
            print('\nLD switching ON, please wait')
            while True:
                if int(self.TSL.Query('POW:STAT?')) == 0:
                    time.sleep(10)
                else:
                    print('\nLD is ON now')
                    break
        else:
            pass

        " Pre-setting Parameters "
        self.TSL.Write('POW:UNIT 0')        # Sets power unit to dBm
        self.TSL.Write('WAV:UNIT 0')        # Sets lambda units to nm
        self.TSL.Write('COHCtrl 0')         # Coherence control off
        self.TSL.Write('POW:ATT:AUT 1')     # Attenuation auto
        self.TSL.Write('POW:ATT 0')
        self.TSL.Write('AM:STAT 0')         # Disables amplitude Modulation
        self.TSL.Write('PW:SHUT 0')         # Opens Internal Shutter
        self.TSL.Write('WAV:SWE 0')

        self.TSL.Write('TRIG:OUTP 3')       # Set trigger output as Step
        self.TSL.Write('TRIG:INP:EXT 0')    # Disable EXT trigger

        " Input parameters "
        PWR = input('\nInput output power: ')
        self.TSL.Write('POW ' + PWR)

        self.TSL.Write('WAV:SWE:MOD 1')     # Sets sweep to continuous mode one way. Needs soft trigger to start the sweep

        WLS = input('\nInput start wavelength: ')
        self.TSL.Write('WAV:SWE:STAR ' + WLS)
        self.TSL.Write('WAV ' + WLS)

        WLE = input('\nInput end wavelength: ')
        self.TSL.Write('WAV:SWE:STOP ' + WLE)

        speed = input('\nInput scan speed: ')
        self.TSL.Write('WAV:SWE:SPE ' + speed)

        self.TSL.Write('WAV:SWE:DEL 0')
        self.TSL.Write('WAV:SWE:CYCL 1')    # Sets repeat cycles to 1 repetition

        step = input('\nInput Step (pm): ')
        step = str(float(step) / 1000)
        self.TSL.Write('TRIG:OUTP:STEP ' + step)

        self.TSL.Write('WAV ' + WLS)
        opc = 0
        while opc == 0:
            opc = self.TSL.Query('*OPC?')
        self.TSL.Write('TRIG:INP:STAN 1')   # Sets TSL in standby mode (executes only one sweep)
        self.TSL.Write('WAV:SWE 1')         # TSL Sweep Status to start
        opc = 0
        time.sleep(0.5)
        while opc == 0:
            opc = self.TSL.Query('*OPC?')
        check2 = self.TSL.Query('WAV:SWE?')

        while check2 != '3':
            check2 = self.TSL.Query('WAV:SWE?')
            time.sleep(0.1)
        self.TSL.Write('WAV:SWE:SOFT')      # Issues Soft Trigger

        print('\nScan started....')

        opc = int(self.TSL.Query('WAV:SWE?'))
        while opc != 0:
            time.sleep(0.05)
            opc = int(self.TSL.Query('WAV:SWE?'))

        print('\nScan done...')

        choice = input("\nDo you want to display wavelength list ( y )?? ")
        if choice == 'y':
            " Outputs the Wavelength list "
            log.Info("Getting TSL wavelength")
            raw = [i / 10000 for i in self.TSL.GetAllDataPointsFromLastScan_SCPICommand()]  # Read LOG data
            round_off = [round(num, 1) for num in raw]
            if len(round_off) == 0:
                log.Info(f"Could not fetch TSL wavelength data, {self.TSL.GetAllDataPointsFromLastScan_SCPICommand()}")
                raise RuntimeError("Could not fetch TSL wavelength data")
            print(round_off)

        log.Info("Device Operations done")


if __name__ == '__main__':
    log = logger.Logger("570")
    tsl570 = TSL570()
    try:
        log.Info("STARTING")
        tsl570.DeviceOperations()
        log.Info("FINISHED")
    except Exception as e:
        log.Critical(f"Unhandled exception in TSL570: {e}")



