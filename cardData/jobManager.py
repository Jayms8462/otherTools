#python .\grabInfo.py -U "https://www.tcdb.com/ViewSet.cfm/sid/222460/1868-Snyder-&-Peck" -D "cards" -H "127.0.0.1" -P "27017"

import random
import subprocess
import paramiko
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import concurrent.futures

load_dotenv(dotenv_path='./login.env')

with open('./urls.txt') as fileData:
    data = fileData.readlines()

def main(url):
    subprocess.run(["python", "C:\\Users\\ajpor\\OneDrive\\desktop\\git\\otherTools\\cardData\\grabInfo.py", "-u", os.getenv('user'), "-p", os.getenv('password'), "-U", url, "-H", "127.0.0.1", "-P", "27017"])
    
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(main, data)


# elif host != "127.0.0.1":
#         hosts.remove(host)
#         print(host, url, hosts)

#         # Creds
#         username = os.getenv('winuser')
#         password = os.getenv('winpassword')

#         # Connect to Server
#         con = paramiko.SSHClient()
#         con.load_system_host_keys()
#         con.connect(host, username=username, password=password)

#         # run the command   
#         stdin, stdout, stderr = con.exec_command('python C:\\Users\\ajpor\\Desktop\git\\otherTools\\cardData\\grabInfo.py -u ' + os.getenv('user') + ' -p ' + os.getenv('password') + ' -U ' + url.replace('\n', '') + ' -H "192.168.1.172" -P "27017"')
#         print("stout", stdout.read())
#         print("sterr", stderr.read())
#         hosts.append(host)