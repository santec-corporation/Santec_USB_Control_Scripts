<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>

> [!NOTE]
> If you have any [Issues](https://github.com/santec-corporation/TSL_USB_Control_Scripts/issues) related to the code, click [Create New](https://github.com/santec-corporation/TSL_USB_Control_Scripts/issues/new) to create a new issue. 


<h1>TSL USB Control Scripts</h1>

![GitHub top language](https://img.shields.io/github/languages/top/santec-corporation/TSL_USB_Control_Scripts?color=blue)

Python Scripts to command and manage Santec TSL Device(s) connected via USB utilizing the Santec_FTDI DLL as the backend. <br>
For all TSL Models. Read below for more information.


<h2>Introduction</h2>

The Santec TSL Devices connected via USB can be controlled using Python scripts with the help of a DLL (Santec_FTDI).

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

  - Once the USB driver is downloaded, make sure that you are able to recognize the TSL-(model) in the System Device Manager.

  - Make sure that you have all the necessary DLLs before running the Python Script(s).



<h2>Major Scripts</h2>

  1) TSL_550_USB.py  -  This script communicates with the TSL with the use of Santec Commands (Command Set-2). <br>
**This script works for TSL-550, TSL-710 devices.

  2) TSL_570_USB.py  -  This script communicates with the TSL with the use of SCPI Commands. <br>
**This script works for TSL-570 devices.


  #### Executable files (.exe)  [ Available in the [Releases](https://github.com/santec-corporation/TSL_USB_Control_Scripts/releases) with the README]
  3) TSL_550_USB.exe  -  This file communicates with the TSL with the use of Santec Commands (Command Set-2). <br>
**This script works for TSL-550, TSL-710 devices.

  4) TSL_570_USB.exe  -  This file communicates with the TSL with the use of SCPI Commands. <br>
**This script works for TSL-570, TSL-770 devices.


  #### Additional Scripts [ In Directory [Additional Scripts](https://github.com/santec-corporation/TSL_USB_Control_Scripts/tree/89912792db0268fdf18e949810e1efa820066026/Additional%20Scripts) ]
  
  5) MULTI_TSL_550_USB.py  -  Example script to control two or more TSL devices. This script communicates with the TSL using Santec Commands (Command Set-2). <br>
**This script works for TSL-550, TSL-710 devices.

  6) SIMUL_MULTI_TSL_550_USB.py  -  Example script to run two or more TSL devices simultaneously at the same time (uses Santec Commands). <br>
**This script works for TSL-550, TSL-710 devices.


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
    
    TSL = ftdi.FTD2xx_helper()              # TSL is an instance to the class FTD2xx_helper
    ```

5) To print the list of connected TSLs with their information (mainly Serial Number),
    Using the properties of the DLL (check the README of the DLL directory for more info)
    ```python
    for i in range(TSL.numDevices):
        print("Device Index: {}".format(i))
        print("Type: {}".format(TSL.ftdiDeviceList[i].Type))
        print("ID: {:x}".format(TSL.ftdiDeviceList[i].ID))
        print("Location ID: {:x}".format(TSL.ftdiDeviceList[i].LocId))
        print("Serial Number: {}".format(TSL.ftdiDeviceList[i].SerialNumber))
        print("Description: {}".format(TSL.ftdiDeviceList[i].Description))
        print("")
    ```

6) Creating a new instance to initialize and control the specific TSL device by passing the Serial Number as a parameter,
    ```python
    TSL = ftdi.FTD2xx_helper('15070009')        # Replace the with the Instrument Serial Number
    ```
    If you have more than one TSL connected,
    ```python
    TSL1 = ftdi.FTD2xx_helper('15070009')       # Replace the with the Instrument Serial Number
    TSL2 = ftdi.FTD2xx_helper('18060009')       # Replace the with the Instrument Serial Number
    .
    .
    TSLn = ftdi.FTD2xx_helper('00000000')
    ```

7) Use the Query() method for querying or reading from the TSL by passing in the instrument command,
    ```python
    TSL.Query('*IDN?')                 # Outputs: SANTEC TSL-(ModelNo.), Serial Number, Version Number
    ```
    
    Moreover, for specifically querying or reading the device identification information, you can use the below method,
    ```python
    TSL.QueryIdn()                     # Outputs: SANTEC TSL-(ModelNo.), Serial Number, Version Number
    ```

8) Use the Write() method for writing to the TSL,
    ```python
    TSL.Write('OP10')                   # Sets the Output power of TSL to 10dBm(or mW)
    ```

9) Reading the Wavelength data from the TSL, <br>

 - For TSL-550, TSL-710, using the GetAllDataPointsFromLastScan_SantecCommand() method,
    ```python
    Wavelength = [i/10000 for i in TSL.GetAllDataPointsFromLastScan_SantecCommand()]          
    print('\nWavelength data of TSL: \n', Wavelength)
    
    # Outputs: 
   Wavelength data of TSL:
   [1500.002, 1500.0958, 1500.2018,........, 1600]
    ```
- For TSL-570, using the GetAllDataPointsFromLastScan_SCPICommand() method,
    ```python
    Wavelength = [i/10000 for i in TSL.GetAllDataPointsFromLastScan_SCPICommand()]          
    print('\nWavelength data of TSL: \n', Wavelength)
    
    # Outputs: 
  Wavelength data of TSL:
  [1500.002, 1500.0958, 1500.2018,........, 1600]
    ```
  
9) To close the USB connection through the FTDI driver, any future commands sent will throw an exception, as the connection is closed,
    ```python
    TSL.CloseUSBConnection()
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

