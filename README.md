<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>


<h1>TSL USB Control Scripts</h1>

Python Scripts to command and manage Santec TSL Device(s) connected via USB utilizing the Santec_FTDI DLL as the backend.


<h2>Introduction</h2>

The Santec TSL Devices connected via USB can be controlled using python scripts with the help of a DLL (Santec_FTDI).

The Santec_FTDI DLL (Santec FTD2xx_helper) is designed to connect to TSL(s) and easily obtain the data points from the previous scan. It uses the FTDI driver for USB communication, and provides simple command line communication with the TSL.


<h2>Requirements</h2>

1) Download the USB Driver ([Driver](https://downloads.santec.com/files/downloadfile/6dbd36cd-a29e-4ca0-a894-8ba4e4fdf0c5)).

2) Once the USB driver is downloaded, make sure that you are able to recognize the TSL-(model) in the System Device Manager.

3) Make sure that you have all the necessary DLLs before running the Python Script(s).


<h2>Major Scripts</h2>
1) TSL_550_USB.py  -  This script communicates with the TSL with the use Santec Commands (Command Set-2).
**This script works for TSL-550, TSL-710 devices.

2) TSL_570_USB.py  -  This script communicates with the TSL with the use SCPI Commands.
**This script works for TSL-570 devices.

3) MULTI_TSL_550_USB.py  -  Example script to control two or more TSL devices. This script communicates with the TSL with the use Santec Commands (Command Set-2).
**This script works for TSL-550, TSL-710 devices.

4) SIMUL_MULTI_TSL_550_USB.py  -  Example script to run two or more TSL devices simultaneously at the same time. (uses Santec Commands)
**This script works for TSL-550, TSL-710 devices.


<h2>DLL List</h2>
1) Santec_FTDI.dll
2) FTD2XX_NET.dll
3) FTDI2XX.dll


<h2>Write your own script</h2>
