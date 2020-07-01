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
tension1 = ch1.voltage*3.2*1.51515
tension2 = ch2.voltage*2*1.5151515
tension3 = ch3.voltage*1.5151515
 #MCP3008 CH0 : Capteur d'Intensité
while True:
    print("(Intensite): " + str(round(ch0.value/100))+"mA")
    print("(Cell 2): {}V ".format((tension1-tension2)))
    print("(Cell 1): {}V ".format((tension2-tension3)))
    print("(Cell 0): {}V ".format(tension3))
    print("(Temp 1): {}°C ".format((ch4.voltage*1.515-0.5)*100))
    print("(Temp 2): {}°C ".format((ch5.voltage*1.515-0.5)*100))
    print("(Temp 3): {}°C ".format((ch6.voltage*1.515-0.5)*100))
    print("(Acc): {}%".format(round((ch7.value/65500)*100)))
    print("--------------------------------------")
    sleep(1)
