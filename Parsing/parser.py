# Ce fichier fait partie du logiciel de gestion de la voiture réalisée par le lycée St Exupéry de Parentis en Born (40160)
# dans le cadre du concours EDUCECO.
#
# L'ensemble du projet est accessible sur github : https://github.com/LabSIStExupery/EducECOCar-Code
#
# Ce programme permet la récupération et l'archivage des données issues des différents capteurs de la voiture vers une base de données MySQL.
# Il est prévu pour être installé sur une raspberry pi 3 connectée à un MCP3008 (Convertisseur Analogique/Numérique) selon le cablâge suivant :
# - MCP3008 CLK vers Pi SCLK
# - MCP3008 DOUT vers Pi MISO
# - MCP3008 DIN vers Pi MOSI
# - MCP3008 CS vers Pi D5
# - MCP3008 VDD vers Pi 5V
# - MCP3008 VREF vers Pi 5V
# - MCP3008 AGND vers Pi GND
# - MCP3008 DGND vers Pi GND
# - MCP3008 CH0 à MCP3008 CH7 vers les différents capteurs analogiques, en suivant l'ordre indiqué plus bas (Initialisation du MCP)
#
# Le fichier de configuration (généré par le script /home/pi/scripts/initConfig.py) contient le délai (en secondes) entre chaque acquisition
# pour chaque capteur, les paramètres de connexion à la base de données, ainsi que les différents paramètres du capteur vitesse.

# Ce programme nécessite :
# - Python 3.7
# - Les libraries Adafruit pour le MCP3008 (https://learn.adafruit.com/mcp3008-spi-adc/python-circuitpython)
# - La library RPi.GPIO installée par défaut sur Raspbian, pour communiquer avec l'unique capteur numérique de vitesse
# - Le connecteur MySQL pour python (Dans le terminal, exécuter "sudo pip3 install mysql-connector-python")
# - Un serveur MySQL/MariaDB et une base de données ayant la structure suivante : https://github.com/LabSIStExupery/EducECOCar-Code/blob/master/EDUCECO.sql

# Quel niveau de débogage ?
#  0 = Désactivé
#  1 = Normal
#  2 = Avancé (Capteur de vitesse)
isDebugOn = 2
# Désactiver le logging externe ? Les logs seront affichés dans l'interpréteur python.
externalLogs = False

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import sys

import mysql.connector
import json
import os
import RPi.GPIO as GPIO
import time

from threading import Thread
from threading import RLock
from adafruit_mcp3xxx.analog_in import AnalogIn
from time import sleep
from math import pi

global actualSpeed
lock = RLock()
connectedToDB = False

msTimestamp = lambda: int(round(time.time() * 1000)) #Permet de générer un Timestamp, en ms.

# Système de logs
# Avant la connexion à la BDD, écrit les logs vers un fichier /home/pi/parser.log
# Une fois connecté, envoie directement les logs à la BDD
if externalLogs:
    sys.stdout = open('/home/pi/logs/parser.log', 'w')

dbLogging = ("INSERT INTO Logs"
                "(Process, TYPE, Message, TIMESTAMP)"
                "VALUES (%s, %s, %s, %s)")

def log(type="info", msg=""):
    if not connectedToDB:
        if type=="info":
            print("[PARSER][INFO] " + msg)
        elif type=="debug" or type=="advDebug":
            if isDebugOn > 0 and not type == "advDebug":
                print("[PARSER][DEBUG] " + msg)
            elif isDebugOn == 2 and type == "advDebug":
                print("[PARSER][DEBUG][SPEED THREAD] " + msg)
        elif type=="warn":
            print("[PARSER][WARNING] " + msg)
        elif type=="critical":
            print("[PARSER][CRITICAL] " + msg)
    else:
        if type=="info":
            cursor.execute(dbLogging, ('PARSER', 'INFO', msg, msTimestamp()))
        elif type=="debug" or type=="advDebug":
            if isDebugOn > 0 and not type=="advDebug":
                cursor.execute(dbLogging, ('PARSER', 'DEBUG', msg, msTimestamp()))
            elif isDebugOn == 2 and type=="advDebug":
                cursor.execute(dbLogging, ('PARSER', 'DEBUG', '[SPEED THREAD] ' + msg, msTimestamp()))
        elif type=="warn":
            cursor.execute(dbLogging, ('PARSER', 'WARNING', msg, msTimestamp()))
        elif type=="critical":
            cursor.execute(dbLogging, ('PARSER', 'CRITICAL', msg, msTimestamp()))
        db.commit()

# Thread pour gérer l'acquisition du capteur vitesse, s'exécutant en parallèle du thread principal.
#  pin = pin de branchement du capteur vitesse
#  diam = diamètre de la roue, en cm
#  trigger = seuil de déclenchement du capteur
#  angle = angle entre deux déclenchements sur la roue, en °
def speedThread(pin, diam, trigger, angle):
    global actualSpeed
    actualSpeed=0
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    lastTime = msTimestamp()
    log("advDebug", "Thread vitesse initialisé.")
    while True:
        diff = trigger + 1
        while diff > trigger:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            sleep(0.000010)
            GPIO.setup(pin, GPIO.IN)
            startTime = round(time.time() * 1000000)
            while(GPIO.input(pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
                diff = round(time.time() * 1000000) - startTime
        turnDelay = msTimestamp() - lastTime
        log("advDebug", "Seuil de déclenchement atteint. Durée depuis le dernier déclenchement : {}ms".format(turnDelay))
        lastTime = msTimestamp()
        with lock:
            actualSpeed = ((pi*diam)/(360/angle))/(turnDelay) * 36
            log("advDebug", "Vitesse enregistrée : {}km/h".format(actualSpeed))
        while diff < trigger:
             GPIO.setup(pin, GPIO.OUT)
             GPIO.output(pin, GPIO.HIGH)
             sleep(0.000010)
             GPIO.setup(pin, GPIO.IN)
             startTime = round(time.time() * 1000000)
             while(GPIO.input(pin) == GPIO.HIGH and round(time.time() * 1000000) - startTime < 3000):
                 diff = round(time.time() * 1000000) - startTime



#Programme principal
log("info","Démarrage de parser.py... Timestamp : {}ms".format(msTimestamp()))

#IINITIALISATION DU MCP(Convertisseur Analogique/Numérique)-------------------------------------------------------
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

ch0 = AnalogIn(mcp, MCP.P0) #MCP3008 CH0 : Capteur d'Intensité
ch1 = AnalogIn(mcp, MCP.P1) #MCP3008 CH1 : Capteur de tension n°1
ch2 = AnalogIn(mcp, MCP.P2) #MCP3008 CH2 : Capteur de tension n°2
ch3 = AnalogIn(mcp, MCP.P3) #MCP3008 CH3 : Capteur de tension n°3
ch4 = AnalogIn(mcp, MCP.P4) #MCP3008 CH4 : Capteur de température n°1
ch5 = AnalogIn(mcp, MCP.P5) #MCP3008 CH5 : Capteur de température n°2
ch6 = AnalogIn(mcp, MCP.P6) #MCP3008 CH6 : Capteur de température n°3
ch7 = AnalogIn(mcp, MCP.P7) #MCP3008 CH7 : Position de l'accélérateur
log("info", "Initialisation du MCP Terminée")
#INITIALISATION DE LA CONFIGURATION------------------------------------------------------------------------------
#Vérifier si le fichier de config existe, sinon le créer
log("debug", "Récupération de la configuration...")
if os.path.exists("/home/pi/config.json"):
    log("debug", "Le fichier de configuration existe")
    pass
else:
    log("critical", "Le fichier de configuration n'existe pas. Veuillez le générer à l'aide du script /home/pi/scripts/initConfig.py")
    exit()

#Chargement du fichier de configuration dans un dictionnaire
try:
    log("debug", "Chargement de la configuration dans un dictionnaire...")
    with open("/home/pi/config.json", 'r') as config:
        conf = json.load(config)
    log("debug", "Terminé")
except:
    log("critical", "Impossible de lire la configuration, vérifiez le fichier /home/pi/config.json. Si besoin, relancez l'utilitaire de création de config /home/pi/scripts/initConfig.py")
    exit()
#Convertir les données
try: 
    log("debug", "Conversion des valeurs...")
    dInt = float(conf['delays']["delayIntensite"])
    dBatt = float(conf['delays']["delayBatterie"])
    dSpeed = float(conf['delays']["delayVitesse"])
    dTemp = float(conf['delays']["delayTemperature"])
    dAcc = float(conf['delays']["delayAccelerateur"])
    dbUser = str(conf['database']["databaseUser"])
    dbName = str(conf['database']["databaseName"])
    dbPwd = str(conf['database']["databasePassword"])
    dbHost = str(conf['database']["databaseHost"])
    wheelDiam = int(conf['speedSensor']['diametreRoue']) 
    ch8Pin = int(conf['speedSensor']['pinBranchementVitesse'])
    triggerValue =  int(conf['speedSensor']['triggerValue'])
    angleValue = int(conf['speedSensor']['angleValue'])
    log("debug", "Terminé")
except ValueError:
    log("critical", "Impossible de convertir les données depuis le fichier /home/pi/config.json, vérifiez vos valeurs.")
    exit()
log("info", "Initialisation de la configuration terminée")
#INITIALISATION DE LA BASE DE DONNEES-------------------------------------------------------------------------------
#Connexion à la BDD
try:
    log("debug", "Tentative de connexion à la BDD avec les paramètres suivants : \n User: {} \n Database: {} \n Password: {} \n Host: {}".format(dbUser,dbName,dbPwd,dbHost))
    db = mysql.connector.connect(user=dbUser, database=dbName, password=dbPwd, host=dbHost)
    cursor = db.cursor()
    log("debug", "Connecté")
except:
    log("critical", "Impossible de se connecter à la base de données. Vérifiez l'état du serveur MariaDB et/ou les paramètres de connexion dans /home/pi/config.json")
    exit()

#Requêtes MYSQL pour mettre à jour la base de donnée, utilisées plus loin
addIntensite = ("INSERT INTO Current"
                "(Current, TIMESTAMP)"
                "VALUES (%s, %s)")

addBatterie = ("INSERT INTO Battery"
                "(Cell1,Cell2,Cell3,TIMESTAMP)"
                "VALUES (%s,%s,%s,%s)")

addVitesse = ("INSERT INTO Speed"
                "(Speed,TIMESTAMP)"
                "VALUES (%s,%s)")

addTemperature = ("INSERT INTO Temperature"
                   "(Temp1, Temp2, Temp3, TIMESTAMP)"
                   "VALUES(%s,%s,%s,%s)")

addAccelerateur = ("INSERT INTO AcceleratorPosition"
                   "(Position, TIMESTAMP)"
                   "VALUES(%s,%s)")
log("info", "Initialisation de la base de données terminée")
if externalLogs:
    log("info", "Basculement du système de logs vers celui de la base de données.")
    connectedToDB = True
log("info", "Initilisation terminée.")
#METTRE A JOUR LA BDD-----------------------------------------------------------------------------------------------
#Lancer l'acquisition de la vitesse en parallèle:
try:
    log("debug", "Lancement du thread secondaire vitesse avec les paramètres suivants : \n Pin du capteur : {} \n Diamètre de la roue : {} \n Seuil de déclenchement : {} \n Angle de mesure : {}".format(ch8Pin, wheelDiam, triggerValue, angleValue))
    thread = Thread(target=speedThread, args=(ch8Pin, wheelDiam, triggerValue, angleValue))
    thread.start()
    log("Thread secondaire vitesse lancé")
except:
    log("critical", "Impossible de lancer le thread secondaire vitesse !")
    exit()

#Mettre à jour la BDD
i = [dInt/0.1, dBatt/0.1, dSpeed/0.1, dTemp/0.1, dAcc/0.1] #Créer un liste contenant le délai (en multiples de 0.1s) pour chaque capteur
log("debug", "Délai des capteurs : \n Intensité : {}s \n Batterie : {}s \n Vitesse : {}s \n Température : {}s \n Position de l'accélérateur : {}s".format(dInt,dBatt,dSpeed,dTemp,dAcc))
while True:
    sleep(0.1)
    for n,null in enumerate(i): #A chaque réitération, attendre 0.1 s et diminuer tous les éléments de la liste de 1
        i[n] += -1
    #Si le "compte à rebours" atteint 0, mettre à jour la table correspondante et remettre le compteur à sa valeur initiale.
    if i[0] == 0:
        log("debug", "Acquisition de l'Intensité")
        cursor.execute(addIntensite, (round(ch0.value*1000), msTimestamp())) #Arrondir l'intensité obtenue en mA
        db.commit()
        log("debug", "Terminé (Valeur:" +str(round(ch0.value*1000)) + ")")
        i[0] = dInt/0.1
    if i[1] == 0:
        log("debug", "Acquisition des tensions de la batterie")
        cursor.execute(addBatterie, (ch1.voltage, ch2.voltage, ch3.voltage, msTimestamp()))
        db.commit()
        log("debug", "Terminé (Valeurs:" + str(ch1.voltage) + " " + str(ch2.voltage) + " " + str(ch3.voltage)  + ")")
        i[1] = dBatt/0.1
    if i[2] == 0:
        log("debug", "Acquisition de la vitesse")
        with lock:
            speed = actualSpeed
        cursor.execute(addVitesse, (speed, msTimestamp())) #Récupérer la vitesse dans le thread parallèle définit plus haut
        log("debug", "Terminé (Valeur: " + str(speed) + "km/h)")
        i[2] = dSpeed/0.1
    if i[3] == 0:
        log("debug", "Acquisition des températures")
        temp4 = (ch4.voltage - 0.5)*100 #Convertir la tension en température pour les 3 capteurs
        temp5 = (ch5.voltage - 0.5)*100
        temp6 = (ch6.voltage - 0.5)*100
        cursor.execute(addTemperature, (temp4, temp5, temp6, msTimestamp()))
        db.commit()
        log("debug", "Terminé (Valeurs:" + str(temp4) + " " + str(temp5) + " " + str(temp6)  + ")")
        i[3] = dTemp/0.1
    if i[4] == 0:
        log("debug", "Acquisition de la position de l'accélérateur")
        cursor.execute(addAccelerateur, (round((ch7.value/1024)*100), msTimestamp())) #Convertir la valeur obtenue en pourcentage
        db.commit()
        log("debug", "Terminé (Valeur:" + str(round((ch7.value/1024)*100)) + ")")
        i[4] = dAcc/0.1