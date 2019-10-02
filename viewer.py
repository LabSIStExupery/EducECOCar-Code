import mysql.connector

try:
    db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=self.database)
    cursor = db.cursor()
except:
    print("Database connection failed")