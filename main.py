# -*- coding: utf-8 -*-

"""
Python script to control Santec Instruments via USB communication
using Santec_FTDI DLL and FTDI USB Driver
Created on Mon Feb 27 18:42:37 2024

@organization: santec holdings corp.
@version: 2.1.0

The current version supports Santec's Instruments connected via USB.
"""

# Basic imports (or dependencies)
import os
import clr
import sys
import time

# Checking and Accessing the DLL (Santec_FTDI) [make sure the DLLs are in the same directory as the script]
assembly_path = r".\DLL"  # device-class path
sys.path.append(assembly_path)
ref = clr.AddReference(r"Santec_FTDI")

# Importing the main method from the DLL
import Santec_FTDI as ftdi

# Calling the FTD2xx_helper class from the Santec_FTDI dll
ftdi_class = ftdi.FTD2xx_helper

# ListDevices() returns the list of all Santec instruments
list_of_devices = ftdi_class.ListDevices()


# Instrument control class
class Santec:
    """
    Santec Instrument control class
    """

    def __init__(self, instrument):
        """
        default parameter initialization
        :parameter instrument - user selected instrument instance
        """
        self.instrument = instrument

    def query(self):
        """
         Queries a command to the instrument inputted by the user
        """
        command = input("\nEnter the command to Query (eg. POW ?) ").upper()
        query = self.instrument.Query(f'{command}')
        time.sleep(0.2)
        print(query)

        return True

    def write(self):
        """
        Writes a command to the instrument inputted by the user
        """
        command = input("\nEnter the command to Write (eg. POW 1) ").upper()
        if self.instrument.Write(f'{command}'):
            print("\nDone")

        return True

    def queryIdn(self):
        """
        Instrument identification query
        """
        print(self.instrument.QueryIdn())

        return True

    def closeConnection(self):
        print("\nClosing instrument USB connection...")
        self.instrument.CloseUsbConnection()

    def gotoMainMenu(self):
        self.closeConnection()
        time.sleep(0.1)
        mainMenu()

    def Exit(self):
        self.closeConnection()
        sys.exit()

    def instrumentMenu(self):
        """
        Menu to select Query, Write or QueryIdn to the instrument
        """
        menu = {
            '1': self.query,
            '2': self.write,
            '3': self.queryIdn,
            '4': self.gotoMainMenu,
            '5': self.Exit
        }
        while True:
            time.sleep(0.2)
            os.system('cls')
            user_operation = input("\nInstrument Menu:-"                                   
                                   "\n1. Query Instrument"
                                   "\n2. Write Instrument"
                                   "\n3. QueryIdn Instrument"
                                   "\n4. Go back"
                                   "\n5. Exit"
                                   "\nSelect an operation: "
                                   )

            if user_operation in menu:
                menu[user_operation]()
            else:
                print("\nInvalid selection.....try again.....")


# Main menu to select to instrument
def mainMenu():
    """
    Main method
    Display the list of detected Santec USB instruments and select an instrument,
    and initializes the Santec control class
     :parameter
     user_select_instrument_number : Example(instrument serial no.) = 15862492, 17834634, 12862492
    """
    # List to store all the detected instruments
    device_list = []

    # Print the Name and Serial number of each detected instrument
    if not list_of_devices:
        print("\nNo instruments found")
    else:
        print("\nDetected Instruments:-")
        for index, device in enumerate(list_of_devices, start=1):
            if device:
                print(f"\n{index}. Device Name: {device.Description},  Serial Number: {device.SerialNumber}")
                device_list.append(device.SerialNumber)

    # Instrument selection and the control class initialization
    while device_list:
        user_select_instrument_number = input("\nEnter the serial number of the instrument to control (eg. 15862492): ")

        if user_select_instrument_number in device_list:
            instrument = ftdi.FTD2xx_helper(user_select_instrument_number)
            print(f"CONNECTION SUCCESSFUL, CONNECTED TO {instrument.QueryIdn()}")
            Santec(instrument).instrumentMenu()
        else:
            print("\nInvalid serial number.....try again.....")


if __name__ == '__main__':
    mainMenu()
