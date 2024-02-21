import sqlite3
import pandas as pd
from datetime import datetime
import re

now = datetime.now()
now = now.strftime("%d/%m/%Y")

pokemon = pd.read_csv("pokemon.csv")

replacements = [
    (" ", "_"),
    ("'", ""),
    (",", " ")
]

#get list of unique types
unique_types = []
for i in pokemon["type1"]:
    if len(unique_types) == 18:
        break
    if i not in unique_types:
        unique_types.append(i)

conn = sqlite3.connect(r"db.sqlite3")
cursor = conn.cursor()

#add types to DB if they don't exist
select_query = "SELECT * FROM baseSite_type"
cursor.execute(select_query)
records = cursor.fetchall()
if not records:
    for type in unique_types:
        conn.execute(f"INSERT INTO baseSite_type (name, date_created, date_updated) VALUES ('{type}', '{now}', '{now}')")
        conn.commit()
    conn.close()

#get type FKs and put into dictionary
select_query = "SELECT id, name FROM baseSite_type"
cursor.execute(select_query)
records = cursor.fetchall()
records_keys = [i[1] for i in records]
records_values = [i[0] for i in records]
type_dict = {records_keys[i]: records_values[i] for i in range(len(records))}
type_dict["no_type"] = 0

def apply_type(row):
    return type_dict[row]

#remove special characters and replace " " in middle of abilities with "_" and separate abilities by " "
def apply_ability(row):
    abilities_split = row.split(",")
    abilities = ""
    for i in abilities_split:
        i = i[1:-1]
        for old, new in replacements:
            i = re.sub(old, new, i)
        abilities += f" {i}"
    return abilities

#secondary_type can be null
def get_secondary_type(value):
    if value == 0:
        return "NULL"
    else:
        return f"'{value}'"

pokemon["type2"] = pokemon["type2"].fillna("no_type")
pokemon["type1ID"] = pokemon["type1"].apply(apply_type)
pokemon["type2ID"] = pokemon["type2"].apply(apply_type)
pokemon["abilities"] = pokemon["abilities"].apply(apply_ability)

select_query = "SELECT * FROM baseSite_pokemon"
cursor.execute(select_query)
records = cursor.fetchall()
if not records:
    for index, row in pokemon.iterrows():
        conn.execute(f"""INSERT INTO baseSite_pokemon (number, name, date_created, date_updated, primaryType_id, 
                secondaryType_id, abilities, generation, attack, defense, special_attack, special_defense, speed, bst_total) 
                VALUES ("{row['pokedex_number']}", "{row['name']}", "{now}", "{now}", "{row['type1ID']}", {get_secondary_type(row['type2ID'])},
                "{row['abilities']}", "{row['generation']}", "{row['attack']}", "{row['defense']}", "{row['sp_attack']}",
                 "{row['sp_defense']}","{row['speed']}", "{row['base_total']}")""")
        conn.commit()
    conn.close()