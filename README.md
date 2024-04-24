<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>

<h1>Santec USB Control Scripts</h1>

USB script to control and command any Santec instrument via USB. <br>

<h2>Introduction</h2>

Santec instruments connected via USB can be managed using the python script with the support of the Santec_FTDI DLL.

The Santec_FTDI DLL is designed to communicate with any Santec instrument and easily obtain the data points of the scan. It uses the FTDI driver for USB communication and provides simple command-line communication with the instruments.

<h2>Scripts</h2>

  - [**main.py**](https://github.com/santec-corporation/Santec_USB_Control_Scripts/blob/santec-python-usb/main.py) - Python script to control and command any Santec instrument.
  - [**matlab_demo_script.m**](https://github.com/santec-corporation/Santec_USB_Control_Scripts/blob/santec-python-usb/matlab_demo_script.m) - Matlab demo script to control and command a TSL instrument. 

<h2>Requirements</h2>

  - [Python](https://www.python.org/) - any version ( latest version **3.12** recommended ), <br>
    download and install the latest version of python from [https://www.python.org/downloads/](https://www.python.org/downloads/), <br>
    to upgrade the existing python package, on your command line, type ``` pip install --upgrade python ```

  - [Pythonnet](https://pypi.org/project/pythonnet/) - any version, <br>
    to install the package, on your command line, type ``` pip install pythonnet ``` or ``` pip3 install pythonnet ``` <br>
    to upgrade existing package, use ``` pip install --upgrade pythonnet ``` <br>
    Make sure you do not have the **clr** package installed. In case to uninstall it, use ``` pip uninstall clr ```

  - Make sure you have the latest Santec USB driver installed on your local machine.

  - Once the USB driver is downloaded, make sure that you are able to recognize the instrument (device) on your machine as a Santec device.

  - Make sure that you have all the necessary DLLs before running the python script. <br><br>


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
    
3) Loading the DLL,
    ```python
    assembly_path = r".\DLL"                                                
    sys.path.append(assembly_path)
    ref = clr.AddReference(r"Santec_FTDI")
    ```

4) Importing the namespace and creating an instance of the FTD2xx_helper class,
    ```python
    import Santec_FTDI as ftdi              # Santec_FTDI is the main namespace
    
    ftdi_class = ftdi.FTD2xx_helper         # Calling the FTD2xx_helper class from the Santec_FTDI dll
    ```

5) Calling the ListDevices method, which returns all detected Santec instruments, 
    ```python
    list_of_devices = ftdi_class.ListDevices()    # ListDevices() returns the list of all active instruments
    ```

6) Print the list of detected instruments, (check the Santec_FTDI dll documentation for more such device properties),
    ```python
    for device in list_of_devices:    
      print('\nDetected Instruments:-')
      print(f'\nDevice Name: {device.Description},  Serial Number: {device.SerialNumber}')
    ```

7) Creating an instrument object,
    ```python
    # Here parameter is the Serial number of the instrument in string format
    instrument = ftdi.FTD2xx_helper(serial_number)    # Instrument Serial Number Example = 23110980, 20208978, 21862492
    ```
    

8) To get the instrument identification string,
    ```python
    idn_query = instrument.QueryIdn()                 # Output: SANTEC INS-(ModelNumber), SerialNumber, VersionNumber
    print(idn_query)
    ```

8) To write a command,
    ```python
    instrument.Write('command')                       # refer to the instrument datasheet for commands
    ```

8) To query a command,
    ```python
    result = instrument.Query('command')              # refer to the instrument datasheet for commands
    print(result)
    ```
    ❗ If the above method does not work, then instead use the Write() followed by Read() method as shown below,
    ```python
    instrument.Write('command')                       # refer to the instrument datasheet for commands
    result = instrument.Read()            
    print(result)
    ```
  
10) Closing the instrument usb connection after use. Any future commands sent will throw an exception, as the connection is already closed,
    ```python
    instrument.CloseUsbConnection()
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
    instrument = Santec_FTDI.FTD2xx_helper(SerialNumber);      % Instrument Serial Number Example = 23110980, 20208978, 21862492
    ```
    

4) To get the instrument identification string,
    ```matlab
    idn_query = instrument.QueryIdn();
    disp(idn_query);                              % Output: SANTEC INS-(ModelNumber), SerialNumber, VersionNumber
    ```

5) To write a command,
    ```matlab
    instrument.Write('command');                  % refer to the instrument datasheet for commands
    ```

6) To query a command,
    ```matlab
    result = instrument.Query('command')          % refer to the instrument datasheet for commands
    disp(result);
    ```
    
    ❗ If the above method does not work, then instead use the Write() followed by Read() method as shown below,
    ```matblab
    instrument.Write('command');                  % refer to the instrument datasheet for commands
    result = instrument.Read();          
    disp(result);
    ```
  
7) Closing the instrument usb connection after use. Any future commands sent will throw an exception, as the connection is already closed,
    ```matlab
    instrument.CloseUsbConnection();
    ```
  </details> 
  
<br>
<details>
<summary><h2>About Santec Swept Test System</h2></summary>

### What is STS IL PDL?
  The Swept Test System is a photonic solution by Santec Corp. to perform Wavelength 
  Dependent Loss characterization of passive optical devices.
  It consists of:
  - A light source: Santec’s Tunable Semiconductor Laser (TSL);
  - A power meter: Santec’s Multi-port Power Meter (MPM);
   

### For more information on the Swept Test System [CLICK HERE](https://inst.santec.com/products/componenttesting/sts)
</details>

