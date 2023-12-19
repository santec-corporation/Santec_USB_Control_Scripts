<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>


<h2>TSL USB Additional Scripts</h2>

  - This is just an example script, the main scripts are in the main directory.

  - Make sure you have the USB Driver, Download the USB Driver ([CLICK HERE](https://downloads.santec.com/files/downloadfile/6dbd36cd-a29e-4ca0-a894-8ba4e4fdf0c5))

  - Once the USB driver is downloaded, make sure that you are able to recognize the TSL-(model) in the System Device Manager.

  - Make sure that you have all the necessary DLLs downloaded before running the Python Script(s).
      - Santec_FTDI.dll
      - FTD2XX_NET.dll
      - FTDI2XX.dll

  - Make sure that the DLL directory containing all the three DLLs are in the same directory as the .exe file after downloading or cloning the project.


<h2>Files</h2>

1) MULTI_TSL_550_USB.py  -  Example script to control two or more TSL devices. This script communicates with the TSL with the use Santec Commands (Command Set-2).
**This script works for TSL-550, TSL-710 devices.

2) SIMUL_MULTI_TSL_550_USB.py  -  Example script to run two or more TSL devices simultaneously at the same time. (uses Santec Commands)
**This script works for TSL-550, TSL-710 devices.
