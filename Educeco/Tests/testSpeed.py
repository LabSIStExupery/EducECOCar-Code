isDebugOn = True
#Activer le débogage avancé ? (Capteur de vitesse)
def debug(msg=""):
    if isDebugOn:
        print("[DEBUG] " + msg)

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP

import mysql.connector
import json
import os
import RPi.GPIO as GPIO
from threading import Thread
from threading import RLock
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
import time
from math import pi
global actualSpeed
class a:
    def getDiff(self):
        #debug("diff > 1000 ; Début de boucle")
        GPIO.setup(ch8pin, GPIO.OUT)
        GPIO.output(ch8pin, GPIO.HIGH)
        sleep(0.000010)
        GPIO.setup(ch8pin, GPIO.IN)
        startTime = round(time.time() * 1000000)
        while(GPIO.input(ch8pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
            diff = round(time.time() * 1000000) - startTime
        #debug("Réception terminée avec diff =" + str(diff))
        return diff
msTimestamp = lambda: int(round(time.time() * 1000)) #Permet de générer un Timestamp, en ms.
ch8pin = 6
wheelDiam = 10
b = a()
if True:
    global actualSpeed
    actualSpeed=0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    debug("Initialisation terminée.")
    while True:
        diff = 3500
        lastTime = msTimestamp()
        debug("Début à : " + str(lastTime) + "ms")
        while b.getDiff() > 1000:
           continue
        turnDelay = msTimestamp() - lastTime
        debug("Temps pour un tour de roue :" + str(turnDelay))
        if turnDelay != 0:
            actualSpeed = (pi*wheelDiam)/(turnDelay) * 36
            debug("ActualSpeed =" + str(actualSpeed))
        while b.getDiff() < 1000:
            continue
