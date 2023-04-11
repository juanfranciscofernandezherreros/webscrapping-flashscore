import mysql.connector
import os

mydb = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )

mycursor = mydb.cursor()

folder_path = './init-mysql'

sql_files = [file for file in os.listdir(folder_path) if file.endswith('.sql')]

for sql_file in sql_files:
    with open(os.path.join(folder_path, sql_file), 'r') as f:
        query = f.read()
    try:
        mycursor.execute(query)
        mydb.commit()
        print(sql_file, "se ha ejecutado correctamente.")
    except mysql.connector.Error as error:
        if "insert" in query.lower():
            print("No se ha podido insertar en el archivo", sql_file, ". Error:", error)
            continue
        else:
            print(sql_file, "no se ha podido ejecutar. Error:", error)

mycursor.close()
mydb.close()
