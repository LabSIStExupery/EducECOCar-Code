import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
 
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
 
# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
while True:
    print("Valeur : {}".format(chan0.value))
    print("Tension divisée(MCP Int): {}".format(chan0.voltage))
    print("Tension  : {}".format(chan0.voltage*3.2*(5/3.3)))
    time.sleep(0.5)
    
