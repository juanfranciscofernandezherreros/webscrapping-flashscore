import datetime
import mysql.connector
from config import DATABASE_CONFIG

# Conecta a la base de datos
cnx = mysql.connector.connect(**DATABASE_CONFIG)

# Obtener la fecha y hora actual en UTC
now_utc = datetime.datetime.utcnow()

# Obtener la fecha de inicio del día actual en UTC
start_utc = datetime.datetime(now_utc.year, now_utc.month, now_utc.day, 0, 0, 0)

# Obtener la fecha de fin del día actual en UTC
end_utc = datetime.datetime(now_utc.year, now_utc.month, now_utc.day, 23, 59, 59)

# Obtener los timestamps en segundos
start_timestamp_utc = int(start_utc.timestamp())
end_timestamp_utc = int(end_utc.timestamp())

# Cursor para ejecutar la consulta
cursor = cnx.cursor()

# Consulta SQL para obtener los registros entre los dos timestamps
query = ("SELECT * FROM matchs "
         "WHERE EventTimeUTC BETWEEN %s AND %s")

# Parámetros para la consulta
query_params = (start_timestamp_utc, end_timestamp_utc)

# Ejecutar la consulta
cursor.execute(query, query_params)

# Obtener los resultados
results = cursor.fetchall()

# Imprimir los resultados
for row in results:
    print(row)

# Cerrar el cursor y la conexión a la base de datos
cursor.close()
cnx.close()

# Imprimir los timestamps
print("Start timestamp (UTC):", start_timestamp_utc)
print("End timestamp (UTC):", end_timestamp_utc)
