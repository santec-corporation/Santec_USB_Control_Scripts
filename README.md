<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>

> [!NOTE]
> If you have any [Issues](https://github.com/santec-corporation/TSL_USB_Control_Scripts/issues) related to the code, click [Create New](https://github.com/santec-corporation/TSL_USB_Control_Scripts/issues/new) to create a new issue. 


<h1>Santec USB Control Scripts</h1>

![GitHub top language](https://img.shields.io/github/languages/top/santec-corporation/TSL_USB_Control_Scripts?color=blue)

Python Scripts to command and manage all Santec Device(s) connected via USB utilizing the Santec_FTDI DLL as the backend. <br>
Read below for more information.


<h2>Introduction</h2>

The Santec Devices connected via USB can be controlled using Python scripts with the help of a DLL (Santec_FTDI).

The Santec_FTDI DLL (Santec FTD2xx_helper) is designed to connect to TSL(s) and easily obtain the data points from the previous scan. It uses the FTDI driver for USB communication and provides simple command-line communication with the TSL.


<h2>Requirements</h2>

  - [Python](https://www.python.org/) - any version ( Latest Version advisable ), <br>
    install the latest version [Python Latest](https://www.python.org/downloads/), <br>
    to upgrade existing one ``` pip install --upgrade python ```

  - [Pythonnet](https://pypi.org/project/pythonnet/) - any version ( Latest Version advisable ), <br>
    to install, use ``` pip install pythonnet ``` or ``` pip3 install pythonnet ``` <br>
    to upgrade existing one ```pip install --upgrade pythonnet```

  - Make sure you have the USB Driver (FTDI D2XX), or you can<br>
    Download the [USB DRIVER](https://downloads.santec.com/files/downloadfile/6dbd36cd-a29e-4ca0-a894-8ba4e4fdf0c5), and follow the [INSTRUCTIONS](https://github.com/santec-corporation/TSL_USB_Control_Scripts/blob/ea5c7f016f391d65151b16d61111f892415adb49/DLL/USB_Driver_Installation.pdf) to install the driver on your local machine.

  - Once the USB driver is downloaded, make sure that you are able to recognize the Instrument (Device) in the System Device Manager.

  - Make sure that you have all the necessary DLLs before running the Python Script(s).


<h2>DLL List</h2>

  - Santec_FTDI.dll
  - FTD2XX_NET.dll
  - FTDI2XX.dll
<br>

<details>
<summary><h2>Writing your own script [Python Demo]</h2> </summary>

1) Make sure that the DLL directory contains all the three DLLs in the same directory as your script.
2) Basic Imports, 
    ```python
    import clr      # Using the 'pythonnet' package, which provides Python bindings for .NET
    import sys      # Using sys to modify the import path to include a specific directory (assembly_path)
    ```
    
3) Accessing the DLL,
    ```python
    assembly_path = r".\DLL"                                                
    sys.path.append(assembly_path)
    ref = clr.AddReference(r"Santec_FTDI")
    ```

4) Importing the namespace and creating an instance to the main class,
    ```python
    import Santec_FTDI as ftdi              # Santec_FTDI is the main namespace
    
    ftdi_class = ftdi.FTD2xx_helper         # Calling the FTD2xx_helper class from the Santec_FTDI dll
    ```

5) Calling the ListDevices method, which returns all detected Santec instruments, 
    ```python
    list_of_devices = ftdi_class.ListDevices()    # ListDevices() returns the list of all Santec instruments
    ```

6) Printing each detected instrument with its name and serial number, (check the Santec_FTDI dll documentation for more device properties),
    ```python
    for device in list_of_devices:    
      print('\nDetected Instruments:-')
      print(f'\nDevice Name: {device.Description},  Serial Number: {device.SerialNumber}')
    ```

7) Initialize a variable for the instrument by calling the FTD2xx_helper class and passing the instrument serial number as a parameter,
    ```python
    instrument = ftdi.FTD2xx_helper(serial_number)    # :parameter Example(instrument serial no.) = 15862492, 17834634, 12862492
    ```
    

8) Print the instrument identification,
    ```python
    instrument.QueryIdn()                     # Output: SANTEC INS-(ModelNo.), Serial_Number, Version_Number
    ```

8) Use the Write() method for writing a command to the instrument,
    ```python
    instrument.Write('command')                   # refer to the instrument datasheet for commands
    ```

8) Use the Query() method for querying a command to the instrument and obtain a response,
    ```python
    result = instrument.Query('command')                   # refer to the instrument datasheet for commands
    print(result)
    ```
  
9) To close the USB connection through the FTDI driver, any future commands sent will throw an exception, as the connection is closed,
    ```python
    instrument.CloseUSBConnection()
    ```
  </details> 
  
<br>
<details>
<summary><h2>About Santec Swept Test System</h2></summary>

### What is STS IL PDL?
  The Swept Test System is the photonic solution by Santec Corp. to perform Wavelength 
  Dependent Loss characterization of passive optical devices.
  It consists of:
  - A light source: Santec’s Tunable Semiconductor Laser (TSL);
  - A power meter: Santec’s Multi-port Power Meter (MPM);
   

### For more information on the Swept Test System [CLICK HERE](https://inst.santec.com/products/componenttesting/sts)
</details>

