import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import mysql.connector 
#MCP INIT
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

ch0 = AnalogIn(mcp, MCP.P0)

#DB INIT
msTimestamp = lambda: int(round(time.time() * 1000))
cnx = mysql.connector.connect(user='test', password='labsi', database='Educeco')
cursor = cnx.cursor()

add_intensite = ("INSERT INTO Intensity "
                "(Value, TIMESTAMP)"
                "VALUES (%s, %s)")
while True:
    cursor.execute(add_intensite, (ch0.value, msTimestamp()))
    time.sleep(1)
    cnx.commit()

