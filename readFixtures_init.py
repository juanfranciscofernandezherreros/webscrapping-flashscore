import csv
import glob
import mysql.connector
import config.database

# Connect to the MySQL server
db = config.database.conectar()

def create_table():
    cursor = db.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'fixtures'
    """)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute("""
            CREATE TABLE fixtures (
                id BIGINT NOT NULL AUTO_INCREMENT,
                EventTimeUTC VARCHAR(255),
                EventTime VARCHAR(255),
                homeTeam VARCHAR(255),
                awayTeam VARCHAR(255),
                matchId VARCHAR(255),
                country VARCHAR(255), 
                competition VARCHAR(255),                                   
                PRIMARY KEY (id)
            );
        """)
    
    cursor.close()


def read_csv_files(csv_files):
    all_data = []
    
    for file in csv_files:
        print("File: " + file)
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')  # Use semicolon as delimiter
            next(reader) # Skip header row
            for row in reader:
                print(row)
                parts1 = row[0]
                parts2 = row[1]
                parts3 = row[2]
                parts4 = row[3]
                parts5 = row[4]     
                parts6 = row[5]                
                parts7 = row[6]                           
                all_data.append([parts1, parts2, parts3, parts4, parts5,parts6,parts7]) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO fixtures (EventTimeUTC, EventTime, homeTeam, awayTeam, matchId,country,competition) \
    VALUES (%s, %s, %s, %s, %s,%s,%s)"

    
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
            print(sql)
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
    csv_files = glob.glob('csv/basketball/fixtures/*.csv')
    all_data = read_csv_files(csv_files)
    
    # Close the database connection
    db.close()
