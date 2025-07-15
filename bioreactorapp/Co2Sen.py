#!/usr/bin/env python3
#Co2Sensor

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def co2Sen():
    values = [0]*8
    for i in range(8):
        values[i] = mcp.read_adc(i)
    #print(values[0])
    return values[0]



# print('Reading mcp3008 values')
# print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
# print('-' * 57)

# while True:
#     co2s=co2Sen()
#     print(co2s)
#     values = [0]*8
#     for i in range(8):
#         values[i] = mcp.read_adc(i)
#     print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
#     time.sleep(0.5)