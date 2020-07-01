import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import sys
import time

from time import sleep

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

ch0 = AnalogIn(mcp, MCP.P0) #MCP3008 CH0 : Capteur d'Intensité
while True:
    print("Raw Voltage CH3: " + str(ch3.voltage*1.515))
    print("Raw Voltage CH4: " + str(ch4.voltage*1.515))
    print("Raw Voltage CH5: " + str(ch5.voltage*1.515))
    sleep(1)