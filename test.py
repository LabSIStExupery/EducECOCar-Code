import mcp3008
import time
with mcp3008.MCP3008() as adc:
    while True:
        print(adc.read([mcp3008.CH0])) # prints raw data [CH0]
        time.sleep(1)
