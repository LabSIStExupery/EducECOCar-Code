import mcp3008
import time 

with mcp3008.MCP3008() as adc:
#adc.read(mcp3008.CH0)
msTimestamp = lambda: int(round(time.time() * 1000))
cnx = mysql.connector.connect(user='root', database='EDUCECO')
cursor = cnx.cursor()

add_intensite = ("INSERT INTO Intensity "
                "(Value, TIMESTAMP)"
                "VALUES (%s, %s)")
while true:
    cursor.execute(add_intensite, (adc.read(mcp3008.CH0), msTimestamp))
    time.sleep(1)
    cnx.commit()

