#!/usr/bin/env python3

import serial
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
gpio_pin = 23
GPIO.setup(gpio_pin, GPIO.OUT)

GPIO.output(gpio_pin, GPIO.LOW)

s = serial.Serial(port="/dev/ttyS0", baudrate=9600, timeout=1)
valOD= [0, 0, 0, 0, 0, 0, 0, 0, 0]   

while True:
    print('Lectura PH')
    
    for i in range(0,9):
        valOD[i] = s.read()
        print (valOD[i])
    time.sleep(1)
