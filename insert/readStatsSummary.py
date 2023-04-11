import csv
import glob
import mysql.connector
import os 
from config import DATABASE_CONFIG

# Connect to the MySQL server
db = mysql.connector.connect(**DATABASE_CONFIG)

def create_table():
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'players'
    """)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute("""
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
                fta VARCHAR(255),
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
        """)
    
    cursor.close()


def read_csv_files(csv_files):
    all_data = []
    
    for file in csv_files:
        print("File: " + file)
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')  # Use semicolon as delimiter
            next(reader) # Skip header row
            for row in reader:
                print(row)
                # Split the row into parts using ',' as a separator
                parts1 = row[0]
                parts2 = row[1]
                parts3 = row[2]
                parts4 = row[3]
                parts5 = row[4]
                parts6 = row[5]
                parts7 = row[6]
                parts8 = row[7]
                parts9 = row[8]
                parts10 = row[9]
                parts11 = row[10]
                parts12 = row[11]
                parts13 = row[12]
                parts14 = row[13]
                parts15 = row[14]
                parts16 = row[15]
                parts17 = row[16]
                parts18 = row[17]
                parts19 = row[18]
                parts20 = row[19]
                parts21 = row[20]
                parts22 = row[21]
                parts23 = row[22]
                parts24 = row[23]
                parts25 = row[24]
                all_data.append([parts1, parts2,parts3,parts4,parts5,parts6,parts7,parts8,parts9,parts10,parts11,parts12,parts13,parts14,parts15,parts16,parts17,parts18,parts19,parts20,parts21,parts22,parts23,parts24,parts25]) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO basketball_game (namePlayer,team,pts,reb,ast,mins,fgm,fga,two_pm,two_pa,three_pm,three_pa,ftm,fta,valoracion,offensiverebounds,deffensiverebounds,personalFours,steals,turnovers,blockedShot,blockedAgains,technicalFouls,playerId,matchId) \
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # Create arrays to store successes and errors
    success_count = 0
    error_count = 0
    successes = []
    errors = []
           
    for row in all_data:
        values = tuple(row)
        cursor = db.cursor()
        
        try:
            cursor.execute(sql, values)
            db.commit()
            success_count += 1
            successes.append(row)
        except mysql.connector.Error as error:
            db.rollback()
            error_count += 1
            errors.append(row)
        finally:
            cursor.close()
            
    print(f"Total Successes: {success_count}, Total Errors: {error_count}")

if __name__ == '__main__':
    create_table()
        
    csv_files = glob.glob('csv/basketball/summary/*.csv')
    all_data = read_csv_files(csv_files)    
    # Close the database connection
    db.close()
