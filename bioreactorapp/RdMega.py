#!/usr/bin/env python3

import serial
import time

ser = serial.Serial(port="/dev/ttyS0", baudrate=9600, timeout=1)
ser.flush()
data = ""
dataV = ['','','','','']


def dovalue(doin):
    try:
        global dataV
        data = ser.readline().decode('utf-8').rstrip()
        if data.strip():
            dataV = data.split(",")
            #print(dataV[1])
            return dataV[1]
        else:
            return doin
    except IndexError:
        return doin
    
def phvalue(phin):
    try:
        global dataV
        data = ser.readline().decode('utf-8').rstrip()
        print(data)
        if data.strip():
            dataV = data.split(",")
            #print(dataV[1])
            return dataV[2]
        else:
            return phin
    except IndexError:
        return phin
    
def tmpvalue(tmpin):
    try:
        global dataV
        data = ser.readline().decode('utf-8').rstrip()
        if data.strip():
            dataV = data.split(",")
            #print(dataV[1])
            return dataV[3]
        else:
            return tmpin
    except IndexError:
        return tmpin
    
    #test fail value
# def failvalue(tmpin):
#     try:
#         global dataV
#         data = ser.readline().decode('utf-8').rstrip()
#         if data.strip():
#             dataV = data.split(",")
#             #print(dataV[1])
#             return dataV[5]
#         else:
#             return tmpin
#     except IndexError:
#         return tmpin
    
# while True:
#     if ser.in_waiting > 0:
#         data = ser.readline().decode('utf-8').rstrip()
#         dataV = data.split(",")    
#     print(dataV[1])
        #print (data)

# # time.sleep(1)
# # ph= phvalue()
# fdo=dovalue("k")
# print(fdo)
# fph=phvalue("j")
# print(fph)
# ftmp=tmpvalue("h")
# print(ftmp)
#     ff=failvalue("h")
#     print(ff)
