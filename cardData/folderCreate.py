import os
import shutil
os.system('cls' if os.name == 'nt' else 'clear')

urls = [
    "c:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\Baseball\\1995 Topps Stadium Club\\Super Team Master Photos - Standard",
    "c:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\Baseball\\1995 Topps Stadium Club\\Virtual Reality - Standard",
    "c:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\Baseball\\1995 Topps Stadium Club\\Virtual Reality Checklist - Standard",
    "c:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\Images\\Baseball\\1995 Topps Stadium Club\\VR Extremist - Standard"
]

os.system('cls' if os.name == 'nt' else 'clear')

for dir in urls:
    files = os.listdir(dir)
    for file in files:
        if file == 'downloadFail.txt':
            continue
        folder = dir + '\\' + file.replace('.jpg', '')
        moveFile = folder + '\\' + file
        fromMove = dir + '\\' + file
        os.mkdir(folder)
        shutil.move(fromMove, folder)
        print(file.replace('.jpg', ''))