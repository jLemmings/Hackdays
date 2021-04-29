import json

import mysql.connector
import ast
import pandas as pd
import geopandas as gpd
import sqlalchemy

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
        df = pd.read_excel(path + "/" + file)
        df[['Datum', 'Wochentag']] = df['Tag'].str.split(" ", expand=True, )
        file_name = file.split(".")[0].replace(" ", "_")
        df.to_sql(file_name, con=engine, if_exists='replace', index=False, index_label=None, chunksize=None, dtype=None,
                  method=None)
        print(f"Wrote {file_name} to DB")


def import_trail_definitions(path):
    trailDefinitons = pd.read_json(path)
    trailDefinitons.gps = trailDefinitons.gps.apply(lambda gps_string: ast.literal_eval(gps_string))
    trailDefinitons.gps = trailDefinitons.gps.apply(lambda gps: LineString([Point(p[0], p[1]) for p in gps]))
    trailDefinitons = gpd.GeoDataFrame(trailDefinitons, geometry=trailDefinitons.gps)
    trailDefinitons = trailDefinitons.drop('gps', axis=1)
    trailDefinitons['geojson'] = trailDefinitons.geometry.apply(lambda geometry: geometry.__geo_interface__)

    cursor.execute("CREATE TABLE IF NOT EXISTS trail_descr(description text, region text, title text, trailId text, geojson text)")
    sql = "INSERT INTO trail_descr (description, region, title, trailId, geojson) VALUES (%s, %s, %s, %s, %s)"

    for i in range(0, len(trailDefinitons)-1):
        row = trailDefinitons.iloc[i]
        test = json.dumps(row[5])
        print(test)
        val = (row[0], row[1], row[2], row[3], test)
        cursor.execute(sql, val)
        mydb.commit()

def import_trails_ridden(path):
    trails = pd.read_json(path)
    engine = create_engine('mysql://root:example@localhost:3307/Bikekingdom')
    trails.to_sql("trails_user", con=engine, if_exists='replace', index=False, index_label=None, chunksize=None, dtype=None,
              method=None)



if __name__ == '__main__':
    import_trails_ridden(
        "C:/Users/annam/OneDrive/Documents/HSLU/MSC/FS21/DC/BikeKingdom/Data/Insidelab Trails/bk_user_trails.json")
