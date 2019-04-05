# Module de lecture/ecriture du port série
import serial
import pymysql.cursors
# Port série ttyACM0
# Vitesse de baud : 9600
# Timeout en lecture : 1 sec
# Timeout en écriture : 1 sec

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='educeco',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        with serial.Serial(port="COM3", baudrate=9600, timeout=1, writeTimeout=1) as port_serie:
            if port_serie.isOpen():
                while True:
                    ligne = port_serie.readline().decode("utf8").replace("\n", "").replace("\r", "")
                    try:
                        intvalue = int(ligne)
                    except:
                        intvalue = 0
                    sql = "INSERT INTO `tests` (`type`, `value`, `unit`) VALUES (\"%s\", \"%d\", \"%s\")" % ("Potentiomètre", intvalue, "/255")
                    cursor.execute(sql)
                    connection.commit()
finally:
    print("finally")