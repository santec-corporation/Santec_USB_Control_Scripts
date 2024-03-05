<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>


<h1>Santec_FTDI (FTD2xx_helper) DLL</h1>

A DLL file written in .NET Framework 4.7.2 which serves as a wrapper to the FTDI DLL, for use with Santec TSL devices connected through USB. 


<h2>Introduction</h2>

The Santec FTD2xx_helper DLL is designed to connect to a TSL and easily obtain the data points from the previous scan. It uses the FTDI driver for USB communication, and provides simple command line communication with the TSL.


<h2>Requirements</h2>

   1) The FTDI2XX driver. Santec can provide a version of this DLL that has been thoroughly tested across various TSL devices. Alternatively, the newest driver can be downloaded from https://ftdichip.com/drivers/d2xx-drivers/ . Once the TSL is connected via USB, you may initially need to update the driver from Device Manager, using the driver files

   2) The FTDI DLL file. This should be the FTDI-provided “FTD2XX_NET.dll” file. This can either be provided by Santec, or from the FTDI site directly, from https://ftdichip.com/software-examples/code-examples/csharp-examples/ . This should NOT be the file “FTDI2XX.dll”, which is also provided by FTDI, but not used by the Santec_FTDI DLL.  For best results, this DLL file should be in the same directory as Santec_FTDI.dll. 

   3) A TSL that supports both USB communication, and either Santec commands or SCPI commands. Please note that Legacy commands are not supported. 


<h2>Prerequisites</h2>

The DLL can be used by any language that can load the .NET DLL and access its functions. This includes languages like Python, C#, PowerShell, MATLAB, etc. 


<h2>Properties</h2>

The Santec_FTDI wrapper contains the following properties

|Property|Description|
|---|---|
|writeCommandTerminator | The final character(s) that are automatically-appended to the end of any command. The default is carriage return, “\r”. The TSL-570 requires “\r”. The TSL 550 doesn’t have a preference.|
|lastConnectedSerialNumber | The most recently connected serial number is automatically set to this property, which allows it to be easily reconnected.|
|ftdi | The internal instance of the FTDI object, which is contained in the wrapped FTDI2XX.dll file. |
|ftdiDeviceList | The internal array of FTDI devices, which is contained in the wrapped FTDI2XX.dll file. |
|EEPROMData | The contents of the device EEPROM. NULL is returned if the device EEPROM cannot be read. |


<h2>Methods</h2>

The Santec_FTDI wrapper contains the following methods

|Method|Description|
|---|---|
|Initialize()<br />Initialize(string deviceSerialNumber) | Initializes and attempts to connect to the TSL. If multiple TSL devices are connected, then Initialize() will connect to one randomly. If you need to connect to a specific TSL, then provide the serial number. <br/> |If the connection fails for any reason, then an exception is thrown.|
|CloseUsbConnection() | Closes the current USB connection through the FTDI driver. Any future commands sent will throw an exception, as the connection is closed.|
|Query(string strCommand) | Send a command to the TSL, and wait for and obtain the response. |
|Write(string strCommand) | Send a command to the TSL. If the command does not end with the writeCommandTerminator, then it is appended automatically. <br />Note that this only sends a command, and does not return any result or confirmation. |
|QueryIdn() | Sends "*IDN?" and returns the response.|
|GetAllDataPointsFromLastScan_SCPICommand() | Get an int[] array of all data points from the last TSL scan. This may take several seconds to retrieve. <br /> This uses the command “READout:DATa?”, and obtains the data from the TSL using little endian format. |
|GetAllDataPointsFromLastScan_SantecCommand() | Get an int[] array of all data points from the last TSL scan. This may take several seconds to retrieve. <br />This uses the command “TA”, and obtains the data from the TSL using big endian format.|


<h2>Example</h2>

```
public static void GetDataPointsExample()
{
    var sftd = new FTD2xx_helper(); //automatically calls the Initialize() method, which connects to the first TSL.
    //var sftd = new FTD2xx_helper("serialNumber"); //automatically calls the Initialize(serialNumber) method, which connects to the TSL containing this serial number.

    //List our devices, just in case we do not know all of our connected devices or serial numbers.
    for (UInt32 i = 0; i < sftd.numDevices; i++)
    {
        Console.WriteLine("Device Index: " + i.ToString());
        Console.WriteLine("Type: " + sftd.ftdiDeviceList[i].Type.ToString());
        Console.WriteLine("ID: " + String.Format("{0:x}", sftd.ftdiDeviceList[i].ID));
        Console.WriteLine("Location ID: " + String.Format("{0:x}", sftd.ftdiDeviceList[i].LocId));
        Console.WriteLine("Serial Number: " + sftd.ftdiDeviceList[i].SerialNumber.ToString());
        Console.WriteLine("Description: " + sftd.ftdiDeviceList[i].Description.ToString());
        Console.WriteLine("");
    }

    Console.WriteLine("IDN = " + sftd.Query("*IDN?\r"));
    Console.WriteLine("Wavelength = " + sftd.Query(":WAVelength? "));

    var dataPoints = sftd.GetAllDataPointsFromLastScan_SCPICommand(); //SCPI is READout:POINts? and READout:DATa?
    //var dataPoints = sftd.GetAllDataPointsFromLastScan_SantecCommand(); //Santec Commands areTN and TA. 

    Console.WriteLine("Retrieved " + dataPoints.Length + " points in.");
    if (dataPoints.Length > 0)
    Console.WriteLine("First data point is " + dataPoints[0]);

}
```
