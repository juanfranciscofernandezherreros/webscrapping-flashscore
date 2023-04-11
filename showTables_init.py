import mysql.connector
from config.database import conectar
# Obtener la conexión a la base de datos
db = conectar()

# Crear un cursor para ejecutar consultas SQL
cursor = db.cursor()

# Ejecutar una consulta SQL
cursor.execute("SELECT table_name, table_rows FROM information_schema.tables WHERE table_schema = 'bigdataetl'")

# Recuperar los resultados de la consulta
resultados = cursor.fetchall()

for tabla in resultados:
    print(f"{tabla[0]} tiene {tabla[1]} filas")

# Cerrar la conexión a la base de datos
db.close()


