import mysql.connector
import csv
from config import DATABASE_CONFIG


# establecer conexión a la base de datos
conn = mysql.connector.connect(**DATABASE_CONFIG)
cur = conn.cursor()

# crear tabla si no existe
cur.execute('''
    CREATE TABLE basketball_game (
        namePlayer VARCHAR(255),
        team VARCHAR(255),
        pts VARCHAR(255),
        reb VARCHAR(255),
        ast VARCHAR(255),
        mins VARCHAR(255),
        fgm VARCHAR(255),
        fga VARCHAR(255),
        two_pm VARCHAR(255),
        two_pa VARCHAR(255),
        three_pm VARCHAR(255),
        three_pa VARCHAR(255),
        ftm VARCHAR(255),
        valoracion VARCHAR(255),
        offensiverebounds VARCHAR(255),
        deffensiverebounds VARCHAR(255),
        personalFours VARCHAR(255),
        steals VARCHAR(255),
        turnovers VARCHAR(255),
        blockedShot VARCHAR(255),
        blockedAgains VARCHAR(255),
        technicalFouls VARCHAR(255),
        playerId VARCHAR(255),
        matchId VARCHAR(255)
    );
''')

# leer el archivo CSV y añadir los datos a la tabla
with open('csv/basketball/summary/GCYmB4Em_stats.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # saltar la fila de encabezado
    for row in reader:
        print(row)
        cur.execute('''
            INSERT INTO basketball_game (
                namePlayer,
                team,
                pts,
                reb,
                ast,
                mins,
                fgm,
                fga,
                two_pm,
                two_pa,
                three_pm,
                three_pa,
                ftm,
                valoracion,
                offensiverebounds,
                deffensiverebounds,
                personalFours,
                steals,
                turnovers,
                blockedShot,
                blockedAgains,
                technicalFouls,
                playerId,
                matchId
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', tuple(row))

        print(cur)

# confirmar cambios y cerrar conexión
conn.commit()
conn.close()
