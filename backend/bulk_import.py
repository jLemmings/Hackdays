import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3307",
    user="root",
    passwd="example",
    database="Bikekingdom"
 )

print(mydb)

cursor = mydb.cursor()