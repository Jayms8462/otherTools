#local = 192.168.1.172
#python .\grabInfo.py -U "https://www.tcdb.com/ViewSet.cfm/sid/222460/1868-Snyder-&-Peck" -D "cards" -H "127.0.0.1" -P "27017"

import random
import subprocess
import paramiko
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path='./login.env')

# hosts = ["192.168.1.81", "127.0.0.1", "192.168.1.209"]
hosts = ["192.168.1.81", "127.0.0.1"]

with open('urls.txt') as fileData:
    data = fileData.readlines()

test = "192.168.1.81"    

if test == "127.0.0.1":
    subprocess.run(["python", "C:\\Users\\ajpor\\OneDrive\\desktop\\git\\otherTools\\cardData\\grabInfo.py", "-u", os.getenv('user'), "-p", os.getenv('password'), "-U", "https://www.tcdb.com/ViewSet.cfm/sid/222460/1868-Snyder-&-Peck", "-D", "cards", "-H", "127.0.0.1", "-P", "27017"])
elif test != "127.0.0.1":
    # Creds
    host = test
    username = os.getenv('winuser')
    password = os.getenv('winpassword')

    # Connect to Server
    con = paramiko.SSHClient()
    con.load_system_host_keys()
    con.connect(host, username=username, password=password)

    # run the command   
    # use the -1 argument so we can split the files by line
    stdin, stdout, stderr = con.exec_command('python C:\\Users\\ajpor\\Desktop\git\\otherTools\\cardData\\grabInfo.py -u ' + os.getenv('user') + ' -p ' + os.getenv('password') + ' -U "https://www.tcdb.com/ViewSet.cfm/sid/222460/1868-Snyder-&-Peck" -D "cards" -H "192.168.1.172" -P "27017"')   

    print(stderr.read())



# for i in data:
#     host = random.choice(hosts)
#     hosts.remove(host)





#     hosts.append(host)