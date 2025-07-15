#!/usr/bin/env python3
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo0_min = 150  # Min pulse length out of 4095
servo0_max = 600  # Max pulse length out of 4095
tst = 4

## ch0 = White
## ch1 = Green
## ch2 = Red
## ch3 = Blue
## ch4 = vaccum pump

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
    
pwm.set_pwm_freq(60)

#print('Change light on channel 0, press Ctrl-C to quit...')

def pwmWhite(inpwt):
    pwm.set_pwm(0, 0, inpwt)

def pwmGreen(inpgn):
    pwm.set_pwm(1, 0, inpgn)

def pwmRed(inprd):
    pwm.set_pwm(2, 0, inprd)
    
def pwmBlue(inpbl):
    pwm.set_pwm(3, 0, inpbl)
    
def pwmPump(inppp):
    pwm.set_pwm(4, 0, inppp)

# while True:
#     pwmGreen(2048)
#     pwmRed(2048)
#     pwmPump(2048)
#     time.sleep(5)
#     pwmGreen(0)
#     pwmRed(0)
#     pwmPump(0)
#     time.sleep(5)

#     # Move servo on channel O between extremes.
#     pwm.set_pwm(tst, 0, 0)
#     time.sleep(1)
#     pwm.set_pwm(tst, 0, 1024)
#     time.sleep(1)
#     pwm.set_pwm(tst, 0, 2048)
#     time.sleep(1)
#     pwm.set_pwm(tst, 0, 3072)
#     time.sleep(1) 
#     pwm.set_pwm(tst, 0, 4095)
#     time.sleep(1)
    
# while True:
#     kit.servo[0].angle = 0

