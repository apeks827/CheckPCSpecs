import subprocess

import win32com.client
import wmi

wmiobj = win32com.client.GetObject("winmgmts:Win32_LogicalDisk.DeviceID='C:'")
c_drive = wmi._wmi_object(wmiobj)
print(c_drive)

completed = subprocess.run(["powershell", "-Command", "Get-PhysicalDisk | ft -AutoSize MediaType"], capture_output=True)
completed = str(completed)
if 'SSD' in completed:
    print('SSD')
else:
    print("HDD or eMMC")
#print(completed)
