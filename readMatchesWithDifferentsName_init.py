import csv
import glob
import mysql.connector
import asyncio
from config import DATABASE_CONFIG

# Connect to the MySQL server
db = mysql.connector.connect(**DATABASE_CONFIG)

async def main(csv_files):
    all_data = []
    print("readDiMatches")
    
    for file in csv_files:
        print("File" + file)
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader) # Skip header row
            for row in reader:
                all_data.append(row) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO matchs (EventTimeUTC, EventTime, HomeTeam, AwayTeam, Quarter1Home, Quarter2Home, Quarter3Home, Quarter4Home, OvertimeHome, Quarter1Away, Quarter2Away, Quarter3Away, Quarter4Away, OvertimeAway, matchId) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
    
    # Create arrays to store successes and errors
    success_count = 0
    error_count = 0
    successes = []
    errors = []
    print(sql)
           
    for row in all_data:
        print("Row" + row[0])
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

async def run():
    csv_files = glob.glob('csv/basketball/results/*.csv')
    await main(csv_files)

if __name__ == '__main__':
    asyncio.run(run())
