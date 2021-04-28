import mysql.connector
import ast
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import os
from sqlalchemy import create_engine, types
import pymysql
pymysql.install_as_MySQLdb()


mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3307",
    user="root",
    passwd="example",
    database="Bikekingdom"
 )

print(mydb)

cursor = mydb.cursor()

def import_bergbahn_data(path):
    # path = "C:/Users/annam/OneDrive/Documents/dev/MSC/Hackdays/data"
    for file in os.listdir(path):
        engine = create_engine('mysql://root:example@localhost:3307/Bikekingdom')
        df = pd.read_excel(path+"/"+file)
        df[['Datum', 'Wochentag']] = df['Tag'].str.split(" ", expand=True,)
        file_name = file.split(".")[0].replace(" ","_")
        df.to_sql(file_name, con=engine, if_exists='replace', index=False, index_label=None, chunksize=None,dtype=None, method=None)
        print(f"Wrote {file_name} to DB")


if __name__ == '__main__':
    import_bergbahn_data("C:/Users/annam/OneDrive/Documents/dev/MSC/Hackdays/data")
