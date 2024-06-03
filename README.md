<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>

<h1>TSL USB Control Scripts</h1>

Python scripts to control and command Santec TSL instruments via USB. <br>
For all TSL models.

<h2>Introduction</h2>

The Santec TSL Devices connected via USB can be controlled using Python scripts with the help of a DLL (Santec_FTDI).

The Santec_FTDI DLL (Santec FTD2xx_helper) is designed to connect to TSL(s) and easily obtain the data points from the previous scan. It uses the FTDI driver for USB communication and provides simple command-line communication with the TSL.


<h2>Requirements</h2>

  - [Python](https://www.python.org/) - any version ( latest version **3.12** recommended ), <br>
    download and install the latest version of python from [https://www.python.org/downloads/](https://www.python.org/downloads/), <br>
    to upgrade the existing python package, on your command line, type ``` pip install --upgrade python ```

  - [Pythonnet](https://pypi.org/project/pythonnet/) - any version, <br>
    to install the package, on your command line, type ``` pip install pythonnet ``` or ``` pip3 install pythonnet ``` <br>
    to upgrade existing package, use ``` pip install --upgrade pythonnet ``` <br>
    Make sure you do not have the **clr** package installed. In case to uninstall it, use ``` pip uninstall clr ```

  - Make sure you have the latest Santec USB driver installed on your local machine.

  - Once the USB driver is downloaded, make sure that you are able to recognize the TSL instrument on your machine as a Santec device.

  - Make sure that you have all the necessary DLLs before running the python script.


<h2>Major Scripts</h2>

  1) TSL_550_USB.py  -  This script communicates with the TSL with the use of Santec Commands (Command Set-2). <br>
    **This script works only with TSL-550, TSL-710 series instruments.

  2) TSL_570_USB.py  -  This script communicates with the TSL with the use of SCPI Commands. <br>
    **This script works only with TSL-570 series instruments.

*Executable files can be found in the releases.


<h2>DLL List</h2>

  - Santec_FTDI.dll
  - FTD2XX_NET.dll
  - FTDI2XX.dll
<br>

<details>
<summary><h2>Write your own script (Python)</h2> </summary>

1) Make sure that the DLL directory is in the same directory as your main script.
2) Basic imports, 
    ```python
    import clr      # This is using the **pythonnet** package, which provides python bindings for .NET Assemblies
    import sys      # Using **sys** to modify the import path to include a specific directory 
    ```
    
3) Loading  the DLL,
    ```python
    assembly_path = r".\DLL"                                                
    sys.path.append(assembly_path)
    ref = clr.AddReference(r"Santec_FTDI")
    ```

4) Importing the namespace and creating an instance to the FTD2xx_helper class,
    ```python
    import Santec_FTDI as ftdi              # Santec_FTDI is the main namespace
    
    TSL = ftdi.FTD2xx_helper()              # TSL is an instance to the class FTD2xx_helper
    ```

5) To print the list of connected TSLs with their information,
    Using the properties of the DLL (check the README in the DLL directory for more info)
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
7) To get the instrument identification string,
    ```python
    TSL.QueryIdn()                     # Outputs: SANTEC TSL-(ModelNo.), Serial Number, Version Number
    ```

8) Use the Query() method for querying or reading from the TSL by passing in the instrument command,
    ```python
    TSL.Query('*IDN?')                 # Outputs: SANTEC TSL-(ModelNo.), Serial Number, Version Number
    ```
   ❗ If the above method does not work, then instead use the Write() followed by Read() method as shown below,
    ```python
    instrument.Write('command')                       # refer to the instrument datasheet for commands
    result = instrument.Read()            
    print(result)
    ```   

9) Use the Write() method for writing to the TSL,
    ```python
    TSL.Write('OP10')                   # Sets the Output power of TSL to 10dBm(or mW)
    ```

10) Reading the Wavelength data from the TSL, <br>

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
  
11) Closing the instrument usb connection after use. Any future commands sent will throw an exception, as the connection is already closed,
    ```python
    TSL.CloseUsbConnection()
    ```
  </details> 

  <details>
<summary><h2>Write your own script (MATLAB)</h2> </summary>

1) Make sure that the DLL directory is in the same directory as your main script.
2) Loading the DLL,
    ```matlab
    folderName = 'DLL';
    dllFileName = 'Santec_FTDI.dll';
    path = fullfile(pwd, folderName, dllFileName);
    NET.addAssembly(path);
    ```
    or
   ```matlab
    path = 'C:\SantecUSBDLL';
    NET.addAssembly([path '\Santec_FTDI.dll']);
    ```

3) Creating an instrument object,
    ```matlab
    % Here parameter is the Serial number of the instrument in string format
    TSL = Santec_FTDI.FTD2xx_helper(SerialNumber);      % Instrument Serial Number Example = 23110980, 20208978, 21862492
    ```
    

4) To get the instrument identification string,
    ```matlab
    idn_query = TSL.QueryIdn();
    disp(idn_query);                              % Output: SANTEC INS-(ModelNumber), SerialNumber, VersionNumber
    ```

5) To write a command,
    ```matlab
    TSL.Write('command');                  % refer to the instrument datasheet for commands
    ```

6) To query a command,
    ```matlab
    result = TSL.Query('command')          % refer to the instrument datasheet for commands
    disp(result);
    ```
    
    ❗ If the above method does not work, then instead use the Write() followed by Read() method as shown below,
    ```matblab
    TSL.Write('command');                  % refer to the instrument datasheet for commands
    result = TSL.Read();          
    disp(result);
    ```
  
7) Closing the instrument usb connection after use. Any future commands sent will throw an exception, as the connection is already closed,
    ```matlab
    TSL.CloseUsbConnection();
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

