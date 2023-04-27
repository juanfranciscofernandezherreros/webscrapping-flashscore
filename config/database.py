import mysql.connector

def conectar():
    # Conectar a la base de datos
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="debezium",
        database="inventory"
    )
    return db