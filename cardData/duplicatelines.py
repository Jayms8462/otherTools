import os
import subprocess

path = "Data"
dir_list = os.listdir(path)

file = "Data/data27.txt"

lines_seen = set()
with open('output.txt', 'w', encoding="utf-8") as output_file:
    for each_line in open(file, 'r', encoding="utf-8"):
        if each_line not in lines_seen:
            output_file.write(each_line)
            lines_seen.add(each_line)
