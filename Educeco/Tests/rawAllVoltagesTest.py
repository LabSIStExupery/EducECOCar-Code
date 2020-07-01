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

ch0 = AnalogIn(mcp, MCP.P0)
ch3 = AnalogIn(mcp, MCP.P3)
ch2 = AnalogIn(mcp, MCP.P2)
ch1 = AnalogIn(mcp, MCP.P1)
ch4 = AnalogIn(mcp, MCP.P4)
ch5 = AnalogIn(mcp, MCP.P5)
ch6 = AnalogIn(mcp, MCP.P6)
ch7 = AnalogIn(mcp, MCP.P7)

 #MCP3008 CH0 : Capteur d'Intensité
while True:
    print("Raw Voltage CH0 (Intensite): " + str(ch0.voltage*1.515))
    print("Raw Voltage CH1 (Cell 0 + 1 + 2 / 3.2): " + str(ch1.voltage*1.515))
    print("Raw Voltage CH2 (Cell 0 + 1 / 2): " + str(ch2.voltage*1.515))
    print("Raw Voltage CH3 (Cell 0): " + str(ch3.voltage*1.515))
    print("Raw Voltage CH4 (Temp 1): " + str(ch4.voltage*1.515))
    print("Raw Voltage CH5 (Temp 2): " + str(ch5.voltage*1.515))
    print("Raw Voltage CH6 (Temp 3): " + str(ch6.voltage*1.515))
    print("Raw Voltage CH7 (Acc): " + str(ch7.voltage*1.515))
    print("--------------------------------------")
    sleep(1)
