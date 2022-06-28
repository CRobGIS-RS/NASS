from importlib.resources import path
import pandas as pd
import os
import mysql.connector
from mysql.connector import errorcode

# Set up DB in MySQL Server
db_connection = mysql.connector.connect(user="mysqlusr", password="C0nn0rc@ll13!")
db_cursor = db_connection.cursor()
#db_cursor.execute("CREATE DATABASE USClimateAgDB;")
db_cursor.execute("USE USClimateAgDB;")

path = "/home/robinsonc6/data/agriculture/"

crops = ['CORN', 'OATS', 'BARLEY', 'SOYBEANS']

for crop in crops:
    # list comprehension
    csv_files = [f for f in os.listdir(path) if f.endswith(f'{crop}.csv')]

    print(csv_files)

    # Create Empty DataFrame
    data = pd.DataFrame(columns=["State", "County", "Year", "Yield_sum", "Yield_mean", "Yield_min", "Yield_max"])
    for csv in csv_files:
        file = os.path.join(path, csv)
        temp_data = pd.read_csv(file, sep=",", index_col=0)
        state =  os.path.basename(csv.replace('.csv','')).split('_',1)[0]
        theme = os.path.basename(csv.replace('.csv','')).rsplit('_',1)[1]
        print(state)
        print(theme)
        temp_data['State'] = f"{state}"
        temp_data['County'] = temp_data['county_name'].str.replace("'s","s").str.title() + ' County'
        temp_data = temp_data[["State", "County", "year", "value_sum", "value_mean", "value_min", "value_max"]]
        temp_data = temp_data.rename(columns={"year":"Year", "value_sum":"Yield_sum",  "value_mean":"Yield_mean", "value_min":"Yield_min",  "value_max":"Yield_max"})
        data = data.append(temp_data, ignore_index=True)


    print(f"Creating table for {theme.title()}, {len(data)} records")

    db_cursor.execute(f"CREATE TABLE {theme.title()}(Id int(11) NOT NULL AUTO_INCREMENT, State varchar(2) NOT NULL, County varchar(50) NOT NULL, Year int(4) NOT NULL,\
                        Yield_sum FLOAT(6,2) NOT NULL, Yield_mean FLOAT(6,2) NOT NULL, Yield_min FLOAT(6,2) NOT NULL, Yield_max FLOAT(6,2) NOT NULL, PRIMARY KEY (`Id`));")

    data_tuples = list(data.itertuples(index=False, name=None))
    for tup in data_tuples:
        print(tup)
        db_cursor.execute(f"INSERT INTO {theme.title()}(State, County, Year, Yield_sum, Yield_mean, Yield_min, Yield_max) VALUES {tup} ;")

db_cursor.execute("FLUSH TABLES;")