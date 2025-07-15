#!/usr/bin/python3
import ms5837
import time

sensor = ms5837.MS5837_30BA() # Default I2C bus is 1 (Raspberry Pi 3)

# We must initialize the sensor before reading it
if not sensor.init():
        #print("Sensor could not be initialized")
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    #print("Sensor read failed!")
    exit(1)



freshwaterDepth = sensor.depth() # default is freshwater
sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor.depth() # No nead to read() again
sensor.setFluidDensity(1000) # kg/m^3

time.sleep(1)

def readPress():
    if sensor.read():
        pressvalue=round(sensor.pressure(),2)
        return pressvalue
    else:
        return 'fail'

# Spew readings
# while True:
#     vps=readPress()
#     print(vps)
