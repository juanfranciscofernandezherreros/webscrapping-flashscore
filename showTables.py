import mysql.connector

# Conectarse a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="user_bigdataetl",
    password="password_bigdataetl",
    database="bigdataetl"
)

# Crear un cursor para ejecutar consultas SQL
cursor = db.cursor()

# Ejecutar una consulta SQL para obtener el número de filas de cada tabla
cursor.execute("SELECT table_name, table_rows FROM information_schema.tables WHERE table_schema = 'bigdataetl'")

# Recuperar los resultados de la consulta
resultados = cursor.fetchall()

# Imprimir el nombre de cada tabla y el número de filas que tiene
for tabla in resultados:
    print(f"{tabla[0]} tiene {tabla[1]} filas")
