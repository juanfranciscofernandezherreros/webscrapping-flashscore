import datetime
import mysql.connector
from config import DATABASE_CONFIG
import asyncio
import playerStatsMatchsSummary


async def main():
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
    matchs_today = cursor.fetchall()

    # Imprimir los timestamps
    print("Start timestamp (UTC):", start_timestamp_utc)
    print("End timestamp (UTC):", end_timestamp_utc)

    # Imprimir los resultados
    for row in matchs_today:
        url = row[1]  # extract the URL string from the first (and only) column of the row
        print(url)
        if url.startswith("g_3_"):
            parts = url.split("_")
            if len(parts) == 3:
                second_part = parts[2]
                await playerStatsMatchsSummary.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/player-statistics/0")
    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    asyncio.run(main())
