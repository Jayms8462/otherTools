import os
from datetime import datetime
import time

file = "data"
ext = ".txt"
fileNum = 20
boolCheck = True

while boolCheck == True:
    with open(file + str(fileNum) + ext, "r", encoding="utf-8") as f:
        if len(f.readlines()) >= 500000:
            fileNum+=1
        else:
            boolCheck = False
    f.close()

with open(file + str(fileNum) + ext, "r", encoding="utf-8") as f:
    print("File:", file + str(fileNum) + ext, "File Count:", len(f.readlines()), "Date/Time:", datetime.now())
f.close()
