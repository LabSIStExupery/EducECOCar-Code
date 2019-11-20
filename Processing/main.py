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
        
def mainLoopProcessing(db, parameters):
    cursor = db.cursor()
    errors = []

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
    
    if percent <= 20:   #Critique : batterie moins de 20 %
        errors.append(["CRITICAL", "BatteryLevel", percent])

    cursor.execute("INSERT INTO PBattery (Percentage, TIMESTAMP) VALUES (%s, %s)", (percent, TS_B))   #Stocke l'info dans la BDD
    db.commit()

    #Instant Power Processing
    cursor.execute("SELECT Current,TIMESTAMP FROM Current ORDER BY TIMESTAMP DESC LIMIT 1")
    data = cursor.fetchone()
    TS_I = data[1]
    I = data[0] / 1000 #mA -> A

    if timestamp() > TS_I + 2000:   #Au dela de 2 secondes on considère les données comme vieilles
        errors.append(["WARNING", "OldData", "Current", timestamp()-TS_I])

    cursor.execute("INSERT INTO PInstantPower (Power, TIMESTAMP) VALUES (%s, %s)", (1.0*total*I, TS_I))   #Stocke l'info dans la BDD
    # SELECT (Battery.Cell1 + Battery.Cell2 + Battery.Cell3)*Current.Current AS Power FROM Battery INNER JOIN Current ON Battery.TIMESTAMP = Current.TIMESTAMP
    db.commit() 
    print(total*I)

    #Calcul de l'autonomie
    cursor.execute("SELECT AVG(Current) FROM Current WHERE TIMESTAMP > %s", (timestamp()-(parameters["AverageOverTime"]*1000))) #Selectionne la moyenne du courant ou tous les TIMESTAMP sont supérieurs au TIMESTAMP actiel moins la durée sur laquelle on se base pour faire la moyenne
    AVGCurrent = cursor.fetchone()[0]   #Consommation moyenne en mAh
    BatteryAuto = parameters["BatteryCapacity"] * percent / 100 #Capacité restante de la batterieen mAh
    Remaining = BatteryAuto / AVGCurrent #Autonomie restante en Heures
    Remaining = Remaining * 60 #Autonomie restante en minutes

    

            
db = mysql.connector.connect(host="news-craft.fr", user="Educeco", passwd="educeco", database="Educeco")

if os.path.exists("../config.json"):
    with open("../config.json", 'r') as f:
        data = f.read()
    
    parameters = json.loads(data)

mainLoopProcessing(db, parameters)

#checker = rangeChecker()
#checker.importJSON("config.json")
#errors = checker.check({"tempMotor" : 149, "tempVariator" : 75})
#print(errors)

db.close()
