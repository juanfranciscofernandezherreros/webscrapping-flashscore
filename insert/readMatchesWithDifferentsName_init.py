import csv
import glob
import mysql.connector
import asyncio

# Connect to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="user_bigdataetl",
    password="password_bigdataetl",
    database="bigdataetl"
)

def create_table():
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'matchs'
    """)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute("""
            CREATE TABLE matchs (
                id BIGINT NOT NULL AUTO_INCREMENT,
                EventTimeUTC INT,
                EventTime VARCHAR(20),
                HomeTeam VARCHAR(50),
                AwayTeam VARCHAR(50),
                Quarter1Home VARCHAR(4),
                Quarter2Home VARCHAR(50),
                Quarter3Home VARCHAR(50),
                Quarter4Home VARCHAR(50),
                OvertimeHome VARCHAR(50),
                Quarter1Away VARCHAR(50),
                Quarter2Away VARCHAR(50),
                Quarter3Away VARCHAR(50),
                Quarter4Away VARCHAR(50),
                OvertimeAway VARCHAR(50),
                matchId VARCHAR(50) UNIQUE,
                PRIMARY KEY (id)
            );

        """)
    
    cursor.close()

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
    create_table()
    csv_files = glob.glob('../csv/basketball/results/*.csv')
    await main(csv_files)

if __name__ == '__main__':
    asyncio.run(run())
