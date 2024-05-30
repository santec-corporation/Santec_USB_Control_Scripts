% This is a demo script 
% to connect and communicate with Santec TSL instrument

clear;
clc;

% Loading the Santec_FTDI dll 
folderName = 'DLL';
dllFileName = 'Santec_FTDI.dll';
path = fullfile(pwd, folderName, dllFileName);
NET.addAssembly(path);


% Creating an instrument object
% here parameter is the Serial number of the instrument
SerialNumber = "12345678";		% Replace with your instrument Serial number
tsl = Santec_FTDI.FTD2xx_helper(SerialNumber);    

% To query the instrument Identification query
idn_query = tsl.QueryIdn();
disp(idn_query);

pause(1);

% To write a command
tsl.Write('POW 5');

pause(1);

% To query any command
tsl.Write('POW?');
pause(0.5);
pow_query = tsl.Read();
output = strtrim(char(double(pow_query)));   % Converts byte_array to readable output
disp(output);

pause(2);

% Closing the instrument usb connection
tsl.CloseUsbConnection();