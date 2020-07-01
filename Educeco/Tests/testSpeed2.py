import RPi.GPIO as GPIO
import time
from time import sleep
isDebugOn = True
#Activer le débogage avancé ? (Capteur de vitesse)
def debug(msg=""):
    if isDebugOn:
        print("[DEBUG] " + msg)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ch8pin = 6
while True:
            debug("diff < 3000 ; Début de boucle")
            GPIO.setup(ch8pin, GPIO.OUT)
            GPIO.output(ch8pin, GPIO.HIGH)
            sleep(0.000010)
            GPIO.setup(ch8pin, GPIO.IN)
            startTime = round(time.time() * 1000000)
            while(GPIO.input(ch8pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
                diff = round(time.time() * 1000000) - startTime
            debug("Réception terminée avec diff =" + str(diff))

