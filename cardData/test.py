import os
import subprocess, platform
import subprocess
import sys

# test = os.popen('systeminfo | findstr /B /C:"OS Name"').read()

# if 'Windows 11' in test:
#     print("Windows 11")
# elif 'Windows 10' in test:
#     print("Windows 10")

if platform.system() == 'Windows':
    print(platform.system().release())