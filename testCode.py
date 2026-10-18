import os
import pygame

os.chdir(os.path.dirname(os.path.abspath(__file__)))
byteString = open("Save_2.txt", "r+")


for line in byteString:
    for i, letter in enumerate(line):
        if letter == ":":
            colonMark = i
    name = line[0 :colonMark + 4]
    data = line[colonMark + 4: -1]
    letters = ""
    bytesData = b""
    '''for letter in data:
        print(bytesData)
        if letter == '\\':
            x = eval(r"" + ("b'" + str(letters) + "'"))
            bytesData += x
            letters = ""
        else:
            letters = letters + letter'''
    
    x = eval(r"" + ("b'" + str(data) + "'"))
    print(type(x))

