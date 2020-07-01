import json
import os
import mysql.connector
import colorama
from colorama import Fore, Style
class notInRange(Exception):
    pass

configFilePath = "../config.json"
print("Vérification de la configuration...\n")
if os.path.exists(configFilePath):
    print(Fore.RED + "Un fichier de configuration a été détecté. Souhaitez vous l'écraser et en générer un nouveau ? (oui/non)\n ")
    ans = input()
    if ans.lower() in ["oui", "o"]:
        print(Fore.GREEN + "\nLancement de l'utilitaire de création de config...")
        pass
    else:
        exit()
else:
    print(Fore.RED + "Le fichier de configuration n'existe pas. Lancement de l'utilitaire de création...")

configFile = {
      'delays':
       {'delayIntensite': 0.0,
        'delayBatterie': 0.0,
        'delayVitesse': 0.0,
        'delayTemperature': 0.0,
        'delayAccelerateur': 0.0},
      'database':
       {'databaseUser': '',
        'databaseName': '',
        'databasePassword': '',
        'databaseHost': ''},
      'speedSensor':
      {'diametreRoue': 0,
       'pinBranchementVitesse': 0,
       'triggerValue': 0,
       'angleValue': 0},
      'ranges':
      {'tempMotor':
        {'allowed':[0,0],
         'warning':[[0,0],[0,0]],
         'critical':[[0,0],[0,0]]},
       'tempVariator':
        {'allowed':[0,0],
         'warning':[[0,0],[0,0]],
         'critical':[[0,0],[0,0]]}
                                },
      'capaciteBatterie':0
                                  }
while True:
    print(Fore.CYAN + "#1 Configuration de la base de donnée------------------------------------------------- \n")
    while True:
        configFile['database']['databaseHost'] = input(Fore.WHITE + "Sur quel serveur la base de données se situe-t-elle ? S'il s'agit du serveur local, entrez 127.0.0.1\n")
        configFile['database']['databaseName'] = input("\nQuel est le nom de la base de données à utiliser ?\n")
        configFile['database']['databaseUser'] = input("\nQuel compte utiliser pour se connecter à la base de données ?\n")
        configFile['database']['databasePassword'] = input("\nMot de passe :\n")

        try:
            print("\nTentative de connexion à la BDD avec les paramètres suivants : \n User: {} \n Database: {} \n Password: {} \n Host: {} \n".format(configFile['database']['databaseUser'],configFile['database']['databaseName'],configFile['database']['databasePassword'],configFile['database']['databaseHost']))
            db = mysql.connector.connect(user=configFile['database']['databaseUser'], database=configFile['database']['databaseName'], password=configFile['database']['databasePassword'], host=configFile['database']['databaseHost'])
            cursor = db.cursor()
            print(Fore.GREEN + "Connexion réussie \n")
            break
        except:
            print(Fore.RED + "La connexion a échoué. Souhaitez vous réessayer ? (oui/non)\n")
            ans = input()
            if ans.lower() in ["oui", "o"]:
                continue
            else:
                break
    print(Fore.CYAN + "\n#2 Configuration des capteurs-------------------------------------------------")
    print(Fore.CYAN + "\n#2.1 Configuration des délais entre chaque acquisition \n")
    while True:
        try:
            configFile['delays']['delayIntensite'] = float(input(Fore.WHITE + "Combien de temps entre chaque acquisition du capteur d'intensité ? (en s)\n"))
            configFile['delays']['delayBatterie'] = float(input("\nCombien de temps entre chaque acquisition des capteurs de tension de la batterie ? (en s)\n"))
            configFile['delays']['delayVitesse'] = float(input("\nCombien de temps entre chaque acquisition du capteur de vitesse ? (en s)\n"))
            configFile['delays']['delayTemperature'] = float(input("\nCombien de temps entre chaque acquisition des capteurs de température ? (en s)\n"))
            configFile['delays']['delayAccelerateur'] = float(input("\nCombien de temps entre chaque acquisition du capteur de la position de l'accélérateur ? (en s)\n"))
            print(Fore.GREEN + "\nCes valeurs vous conviennent-elles ? (oui/non) \n Délai intensité : {} \n Délai Batterie : {} \n Délai Vitesse : {} \n Délai Température : {} \n Délai Accélérateur : {} \n".format(configFile['delays']['delayIntensite'], configFile['delays']['delayBatterie'], configFile['delays']['delayVitesse'], configFile['delays']['delayTemperature'], configFile['delays']['delayAccelerateur']))
            ans = input()
            if ans.lower() in ["oui", "o"]:
                break
            else:
                continue
        except ValueError:
            print(Fore.RED + "[ERREUR] Veuillez entrer un nombre à virgule.")
            continue
    print(Fore.CYAN + "\n#2.2 Configuration du capteur de vitesse \n")
    while True:
        try:
            configFile['speedSensor']['diametreRoue'] = float(input(Fore.WHITE + "Quel est le diamètre de la roue ? (en cm)\n"))
        except ValueError:
            print(Fore.RED + "[ERREUR] Veuillez entre un nombre à virgule")
            continue
        try:
            configFile['speedSensor']['pinBranchementVitesse'] = int(input("\nSur quel pin numérique le capteur de vitesse est-il branché ?\n"))
            configFile['speedSensor']['triggerValue'] = int(input("\nQuel est le seuil de déclenchement du capteur vitesse ? (en µs)\n"))
            configFile['speedSensor']['angleValue'] = int(input("\nQuel angle sépare deux déclenchements du capteur sur la roue ? (en °)\n"))
            if configFile['speedSensor']['angleValue'] > 360 or configFile['speedSensor']['diametreRoue'] < 0:
                raise notInRange()
        except ValueError:
            print(Fore.RED + "[ERREUR] Veuillez entre un nombre entier")
            continue
        except notInRange:
            print(Fore.RED + "[ERREUR] L'angle doit être compris entre 0 et 360°")
            continue
        print(Fore.GREEN + "\nCes valeurs vous conviennent-elles ? (oui/non) \n Diamètre Roue : {} \n Pin  de branchement : {} \n Seuil de déclenchement : {} \n Angle : {} \n".format(configFile['speedSensor']['diametreRoue'], configFile['speedSensor']['pinBranchementVitesse'], configFile['speedSensor']['triggerValue'], configFile['speedSensor']['angleValue']))
        ans = input()
        if ans.lower() in ["oui", "o"]:
            break
        else:
            continue
    print(Fore.CYAN + "\n#3 Configuration des plages de sécurité-------------------------------------------------")
    print(Fore.CYAN + "\n#3.1 Configuration des plages du moteur")
    while True:
        try:
            print(Fore.CYAN + "\n#3.1.1 Plage normale de fonctionnement :")
            nMin = int(input(Fore.WHITE + "Température minimale :\n"))
            nMax = int(input("\nTempérature maximale :\n"))
            configFile['ranges']['tempMotor']['allowed'][0] = nMin
            configFile['ranges']['tempMotor']['allowed'][1] = nMax
            configFile['ranges']['tempMotor']['warning'][0][1] = nMin
            configFile['ranges']['tempMotor']['warning'][1][0] = nMax
            print(Fore.CYAN + "\n#3.1.2 Plages anormales de fonctionnement et nécéssitant une attention particulière :")
            wMin  = int(input(Fore.WHITE + "Température anormale minimale en dessous de " + str(nMin) + " :\n"))
            wMax = int(input("\nTempérature anormale maximale au dessus de " + str(nMax) + " :\n"))
            configFile['ranges']['tempMotor']['warning'][0][0] = wMin
            configFile['ranges']['tempMotor']['warning'][1][1] = wMax
            configFile['ranges']['tempMotor']['critical'][0][1] = wMin
            configFile['ranges']['tempMotor']['critical'][1][0] = wMax
            print(Fore.CYAN + "\n#3.1.3 Plages critiques de fonctionnement :")
            cMin = int(input(Fore.WHITE + "Température critique minimale en dessous de " + str(wMin) + " :\n"))
            cMax = int(input("\nTempérature critique maximale au dessus de " + str(wMax) + " :\n"))
            configFile['ranges']['tempMotor']['critical'][0][0] = cMin
            configFile['ranges']['tempMotor']['critical'][1][1] = cMax
            print(Fore.GREEN + "\nCes valeurs vous conviennent-elles ? (oui/non) \n Fonctionnement normal : [{0},{1}] \n Fonctionnement anormal : [{2},{0}],[{1},{3}] \n Fonctionnement critique : [{4},{2}],[{3},{5}] \n".format(nMin,nMax,wMin,wMax,cMin,cMax))
            ans = input()
            if ans.lower() in ["oui", "o"]:
                break
            else:
                continue
        except ValueError:
            print(Fore.RED + "[ERREUR] Veuillez entrer un nombre entier.")
            continue

    print(Fore.CYAN + "\n#3.2 Configuration des plages du variateur \n")
    while True:
        try:
            print(Fore.CYAN + "#3.2.1 Plage normale de fonctionnement : ")
            nMin = int(input(Fore.WHITE + "Température minimale :\n"))
            nMax = int(input("\nTempérature maximale :\n"))
            configFile['ranges']['tempVariator']['allowed'][0] = nMin
            configFile['ranges']['tempVariator']['allowed'][1] = nMax
            configFile['ranges']['tempVariator']['warning'][0][1] = nMin
            configFile['ranges']['tempVariator']['warning'][1][0] = nMax
            print(Fore.CYAN + "\n#3.2.2 Plages anormales de fonctionnement et nécéssitant une attention particulière :")
            wMin  = int(input(Fore.WHITE + "Température anormale minimale en dessous de " + str(nMin) + " :\n"))
            wMax = int(input("\nTempérature anormale maximale au dessus de " + str(nMax) + " :\n"))
            configFile['ranges']['tempVariator']['warning'][0][0] = wMin
            configFile['ranges']['tempVariator']['warning'][1][1] = wMax
            configFile['ranges']['tempVariator']['critical'][0][1] = wMin
            configFile['ranges']['tempVariator']['critical'][1][0] = wMax
            print(Fore.CYAN + "\n#3.2.3 Plages critiques de fonctionnement :")
            cMin = int(input(Fore.WHITE + "Température critique minimale en dessous de " + str(wMin) + " :\n"))
            cMax = int(input("\nTempérature critique maximale au dessus de " + str(wMax) + " :\n"))
            configFile['ranges']['tempVariator']['critical'][0][0] = cMin
            configFile['ranges']['tempVariator']['critical'][1][1] = cMax
            print(Fore.GREEN + "\nCes valeurs vous conviennent-elles ? (oui/non) \n Fonctionnement normal : [{0},{1}] \n Fonctionnement anormal : [{2},{0}],[{1},{3}] \n Fonctionnement critique : [{4},{2}],[{3},{5}] \n".format(nMin,nMax,wMin,wMax,cMin,cMax))
            ans = input()
            if ans.lower() in ["oui", "o"]:
                break
            else:
                continue
        except ValueError:
            print(Fore.RED + "[ERREUR] Veuillez entrer un nombre entier.")
            continue
    print(Fore.CYAN + "\n#4 Autres configurations\n")
    while True:
        try:
            configFile['capaciteBatterie'] = int(input("Quelle est la capacité de la batterie (en mA) ?\n"))
            break
        except ValueError:
            print(Fore.RED + "[ERREUR] Veuillez entrer un nombre entier")
            continue
    print(Fore.CYAN + "\n#5 Recapitulatif ------------------------- \n")
    print(json.dumps(configFile, indent=2))
    print(Fore.GREEN + "\n Ces valeurs vous conviennent-elles ? (oui/non)\n")
    ans = input()
    if ans.lower() in ["oui", "o"]:
        break
    else:
        continue

with open(configFilePath, 'w') as outfile:
    json.dump(configFile, outfile, indent=4)

print(Fore.GREEN + "\nLe fichier a été enregistré avec succès !")
