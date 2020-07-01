from threading import Thread
from time import sleep
import parser
import processing
print("[START] Launching parser.py")
Thread(target = parser.parser).start()
print("[START] Done. Waiting for 3 seconds...")
sleep(3)
print("[START] Launching processing.py")
Thread(target = processing.processing).start()
print("[START] Done.")


