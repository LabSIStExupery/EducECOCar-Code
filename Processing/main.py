import mysql.connector
import time
import json
import os

timestamp = lambda: int(round(time.time() * 1000))

class rangeChecker():
    def __init__(self, ranges={}):
        self.ranges = ranges

    def importJSON(self, path):
        if not os.path.exists(path):
            return -1

        with open(path, 'r') as f:
            data = f.read()
        
        rawRanges = json.loads(data)["ranges"]

        for name, r in rawRanges.items():
            self._addRange(name, r)

    def _addRange(self, name, ranges):
        self.ranges[name] = ranges

    def checkOne(self, name, value):
        errors = []
        if name not in self.ranges.keys():
            errors.append(["nameError", name])
            return errors
        if value in self.ranges[name]["allowed"]:
            return errors
        else:
            for warning in self.ranges[name]["warning"]:
                if value > warning[0] and value < warning[1]:
                    errors.append(["WARNING", name, warning, value])
                    return errors
            for critical in self.ranges[name]["critical"]:
                if value > critical[0] and value < critical[1]:
                    errors.append(["CRITICAL", name, critical, value])
                    return errors
        return ["noErrorError"]

    def check(self, values):
        errors = []
        if not type(values) is dict:
            errors.append(["typeError"])
            return errors

        for name, value in values.items():
            if not name in self.ranges.keys():
                errors.append(["nameError", name])
                continue

            if not value in self.ranges[name]["allowed"]:
                for warning in self.ranges[name]["warning"]:
                    if value > warning[0] and value < warning[1]:
                        errors.append(["WARNING", name, warning, value])
                for critical in self.ranges[name]["critical"]:
                    if value > critical[0] and value < critical[1]:
                        errors.append(["CRITICAL", name, critical, value])
        return errors

    def dumpRanges(self):
        for name, r in self.ranges.items():
            print(name, r)
        

if os.path.exists("../config.json"):
    with open("../config.json", 'r') as f:
        data = f.read()
    
    parameters = json.loads(data)
            
db = mysql.connector.connect(host=parameters["database"]["databaseHost"], user=parameters["database"]["databaseUser"], passwd=parameters["database"]["databasePassword"], database=parameters["database"]["databaseName"])

cursor = db.cursor()
errors = []

while True:    
    ### === PROCESSING === ###
    #Battery level processing
    cursor.execute("SELECT Cell1,Cell2,Cell3,TIMESTAMP FROM Battery ORDER BY TIMESTAMP DESC LIMIT 1") #Selectionne la dernière entrée de batterie dans la BDD
    data = cursor.fetchone()
    TS_B = data[3]
    cells = [data[0],data[1],data[2]]

    if timestamp() > TS_B+2000:  #Au dela de 2 secondes on considère les données comme vieilles
        errors.append(["WARNING", "OldData", "Battery", timestamp()-TS_B])

    total = cells[0] + cells[1] + cells[2] #Tension totale aux bornes de la batterie
    if total < 10.8:    #Cas 1 : batterie moins de 10%
        percent = (total - 9) * 5.55
    elif total >= 10.8 and total < 11.91:   #cas 2 : Batterie moins de 80%
        percent = (total - 10.8) * 63.06 + 10
    elif total >= 11.91:    #Cas 3 : Batterie plus de 80%
        percent = (total - 11.91) * 28.98 + 80

    cursor.execute("INSERT INTO PBattery (Percentage, TIMESTAMP) VALUES (%s, %s)", (percent, TS_B))   #Stocke l'info dans la BDD
    print("[PROCESSING] Pourcentage Batterie : {}%".format(percent))
    #Instant Power Processing
    cursor.execute("SELECT (Battery.Cell1 + Battery.Cell2 + Battery.Cell3)*Current.Current AS Power FROM Battery INNER JOIN Current ON Battery.TIMESTAMP = Current.TIMESTAMP")

    #Calcul de l'autonomie
    print((timestamp()-(parameters["AverageOverTime"]*1000)))
    cursor.execute("SELECT AVG(Current) FROM Current WHERE TIMESTAMP > " + str(timestamp()-(  parameters["AverageOverTime"]*1000))) #Selectionne la moyenne du courant ou tous les TIMESTAMP sont supérieurs au TIMESTAMP actiel moins la durée sur laquelle on se base pour faire la moyenne
    AVGCurrent = cursor.fetchone()[0]   #Consommation moyenne en mAh
    BatteryAuto = parameters["BatteryCapacity"] * percent / 100 #Capacité restante de la batterieen mAh
    Remaining = BatteryAuto / AVGCurrent * 60 #Autonomie restante en minutes
    cursor.execute("INSERT INTO PAutonomy (Time, TIMESTAMP) VALUES (%s, %s)", (Remaining, timestamp()))
    print("[PROCESSING] Autonomie restante : {}m".format(Remaining))
    #Calcul de la distance parcourue
    cursor.execute("SELECT AVG(Speed) FROM Speed") # Vitesse moyenne tout au long de la course
    AVGSpeed = cursor.fetchone()[0]

    cursor.execute("SELECT TIMESTAMP FROM Speed ORDER BY TIMESTAMP ASC LIMIT 1") # Premier TIMESTAMP enregistré
    FirstTS = cursor.fetchone()[0]

    cursor.execute("SELECT TIMESTAMP FROM Speed ORDER BY TIMESTAMP DESC LIMIT 1") # Dernier TIMESTAMP enregistré
    LastTS = cursor.fetchone()[0]

    if timestamp() > LastTS + 2000:   #Au dela de 2 secondes on considère les données comme vieilles
        errors.append(["WARNING", "OldData", "Speed", timestamp()-LastTS])

    Duration = ((LastTS - FirstTS) / 1000) / 3600 # Temps de course depuis le début en heures
    Distance = Duration * AVGSpeed # Distance parcourue en km
    cursor.execute("INSERT INTO PDistance (Distance, TIMESTAMP) VALUES (%s, %s)", (Distance, timestamp()))
    print("[PROCESSING] Distance parcourue : {}km".format(Distance))
    db.commit()


    ### === ERRORS === ###
    #Battery
    if percent <= 20:   #Critique : batterie moins de 20 %
        errors.append(["CRITICAL", "BatteryLevel", percent])

    #Global Ranges checking
    cursor.execute("SELECT Speed FROM Speed ORDER BY TIMESTAMP DESC LIMIT 1") # Derniere vitesse relevée
    Speed = cursor.fetchone()[0]
    cursor.execute("SELECT Current FROM Current ORDER BY TIMESTAMP DESC LIMIT 1") # Derniere Intensité relevée
    Current = cursor.fetchone()[0]
    cursor.execute("SELECT Temp1,Temp2,Temp3,TIMESTAMP FROM Temperature ORDER BY TIMESTAMP DESC LIMIT 1") # Dernieres Températures relevées
    data = cursor.fetchone()
    tempMotor = data[0]
    tempVariator = data[1]
    tempBattery = data[2]
    TS_Temp = data[3]

    if timestamp() > LastTS + 2000:   #Au dela de 2 secondes on considère les données comme vieilles
        errors.append(["WARNING", "OldData", "Temperature", timestamp()-TS_Temp])

    checker = rangeChecker()
    checker.importJSON("../config.json")
    RangeErrors = checker.check({"tempMotor" : tempMotor, "tempVariator" : tempVariator, "tempBattery" : tempBattery, "speed" : Speed, "current" : Current})
    errors = errors + RangeErrors
    print(errors)

db.close()
