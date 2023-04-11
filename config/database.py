import mysql.connector

def conectar():
    # Conectar a la base de datos
    db = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )
    return db
