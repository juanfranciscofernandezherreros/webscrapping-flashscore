import mysql.connector
import os
import config.database

# Connect to the MySQL server
db = config.database.conectar()

mycursor = db.cursor()

folder_path = './init-db'

sql_files = [file for file in os.listdir(folder_path) if file.endswith('.sql')]

for sql_file in sql_files:
    with open(os.path.join(folder_path, sql_file), 'r') as f:
        query = f.read()
    try:
        mycursor.execute(query)
        db.commit()
        print(sql_file, "se ha ejecutado correctamente.")
    except mysql.connector.Error as error:
        print(sql_file, "no se ha podido ejecutar. Error:", error)
        

mycursor.close()
db.close()