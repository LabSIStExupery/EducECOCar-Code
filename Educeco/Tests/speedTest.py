import RPi.GPIO as GPIO
from math import pi
angle = 60
import time
from time import sleep
trigger = 1000
global actualSpeed
actualSpeed=0
msTimestamp = lambda: int(round(time.time() * 1000)) #Permet de générer un Timestamp, en ms.
diam = 40 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lastTime = msTimestamp()
pin = 6
print("advDebug", "Thread vitesse initialisé.")
#while True:
#    diff = trigger + 1
#    while diff > trigger: #On envoie une impulsion au capteur pendans 10µs. Ensuite, le capteur renvoie une tension pendant une certaine durée. Si cette durée est supérieure au seuil de déclenchement fixé, 
#        GPIO.setup(pin, GPIO.OUT) # alors cela signifie que le capteur a détecté quelque chose. On enregistre donc le temps qu'il a mis depuis le dernier déclenchement (variable turnDelay) et, en fonction 
#        GPIO.output(pin, GPIO.HIGH) #de l'angle parcourue et du périmètre de la roue, en déduit la distance parcourue et donc la vitesse. Enfin, on attend que le capteur redescende en dessous du seuil
#        sleep(0.000010) # de déclenchement et on recommence.
#        GPIO.setup(pin, GPIO.IN)
#        startTime = round(time.time() * 1000000)
#        while(GPIO.input(pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
#           diff = round(time.time() * 1000000) - startTime
#        print("Diff = {}".format(diff))
 

actualSpeed=0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
lastTime = msTimestamp()
print("advDebug", "Thread vitesse initialisé.")
while True:
    diff = trigger + 1
    while diff > trigger: #On envoie une impulsion au capteur pendans 10µs. Ensuite, le capteur renvoie une tension pendant une certaine durée. Si cette durée est supérieure au seuil de déclenchement fixé, 
        GPIO.setup(pin, GPIO.OUT) # alors cela signifie que le capteur a détecté quelque chose. On enregistre donc le temps qu'il a mis depuis le dernier déclenchement (variable turnDelay) et, en fonction 
        GPIO.output(pin, GPIO.HIGH) #de l'angle parcourue et du périmètre de la roue, en déduit la distance parcourue et donc la vitesse. Enfin, on attend que le capteur redescende en dessous du seuil
        sleep(0.000010) # de déclenchement et on recommence.
        GPIO.setup(pin, GPIO.IN)
        startTime = round(time.time() * 1000000)
        while(GPIO.input(pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
            diff = round(time.time() * 1000000) - startTime
    turnDelay = msTimestamp() - lastTime
    print("advDebug", "Seuil de déclenchement atteint. Durée depuis le dernier déclenchement : {}ms".format(turnDelay))
    lastTime = msTimestamp()
    actualSpeed = round((((pi*diam)/(360/angle))/(turnDelay) * 36),3)
    print("advDebug", "Vitesse enregistrée : {}km/h".format(actualSpeed))
    while diff < trigger:
         GPIO.setup(pin, GPIO.OUT)
         GPIO.output(pin, GPIO.HIGH)
         sleep(0.000010)
         GPIO.setup(pin, GPIO.IN)
         startTime = round(time.time() * 1000000)
         while(GPIO.input(pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
             diff = round(time.time() * 1000000) - startTime
