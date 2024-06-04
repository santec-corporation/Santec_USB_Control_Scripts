<p align="right"> <a href="https://www.santec.com/jp/" target="_blank" rel="noreferrer"> <img src="https://www.santec.com/dcms_media/image/common_logo01.png" alt="santec" 
  width="250" height="45"/> </a> </p>


<h2>TSL USB Additional Scripts</h2>

  - This is just an example script.

  - Make sure you have the latest Santec USB driver installed on your local machine.

  - Once the USB driver is downloaded, make sure that you are able to recognize the TSL instrument on your machine as a Santec device.

  - Make sure that you have all the necessary DLLs before running the python script.
      - Santec_FTDI.dll
      - FTD2XX_NET.dll
      - FTDI2XX.dll

  - Make sure that the DLL directory is in the same directory as your main script.


<h2>Files</h2>

1) MULTI_TSL_550_USB.py  -  Example script to control two or more TSL instruments. This script communicates with the TSL instrument using Santec Commands (Command Set-2).
**This script only with TSL-550, TSL-710 series instruments.

2) SIMUL_MULTI_TSL_550_USB.py  -  Example script to control two or more TSL instruments simultaneously at the same time. (uses Santec Commands)
**This script only with TSL-550, TSL-710 series instruments.
