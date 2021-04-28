from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, types
import pymysql
pymysql.install_as_MySQLdb()
mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3307",
    user="root",
    passwd="example"
 )
cursor = mydb.cursor()
print(mydb)

app = Flask(__name__)
api = Api(app)

class Bergbahn(Resource):
    def get(self):
        argument = request.args
        print(argument)
        name = request.args.get("name")
        print(name)
        stunde = request.args.get("stunde")
        print(stunde)
        wochentag = request.args.get("wochentag")
        all_hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        string_all_hours = str(tuple([key for key in all_hours])).replace(',)', ')')
        all_days = ["Mo","Di","Mi","Do","Fr","Sa","So"]
        string_all_days = str(tuple([key for key in all_days])).replace(',)', ')')
        if name == None:
            raise ValueError
            print("Name must be given")
        if stunde != None:
            stunde = [int(stunde)]
            stunde = str(tuple([key for key in stunde])).replace(',)', ')')
        else:
            stunde = string_all_hours
        if wochentag != None:
            wochentag = [wochentag]
            wochentag = str(tuple([key for key in wochentag])).replace(',)', ')')
        else:
            wochentag = string_all_days
        name= name.replace("'", "")
        print(name)
        print(stunde)
        print(wochentag)
        engine = create_engine('mysql://root:example@localhost:3307/Bikekingdom')
        sql_statement = f"SELECT * FROM Bikekingdom.{name} WHERE stunde IN  {stunde} and wochentag IN {wochentag}"
        cursor.execute(sql_statement)
        data = cursor.fetchall()
        return {'data' : data}, 200


# Add URL endpoints
api.add_resource(Bergbahn,'/bergbahn')


if __name__ == '__main__':
    app.run()