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
        WHERE table_name = 'stats_match'
    """)
    
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute("""
            CREATE TABLE stats_match (
            id BIGINT NOT NULL AUTO_INCREMENT,
            namePlayer VARCHAR(200),
            team VARCHAR(200),	
            pts VARCHAR(200),	
            reb VARCHAR(200),	
            ast VARCHAR(200),	
            min VARCHAR(200),	
            fgm VARCHAR(200),	
            fga VARCHAR(200),	
            2pm VARCHAR(200),	
            2pa VARCHAR(200),	
            3pm VARCHAR(200),
            3pa VARCHAR(200),
            ftm VARCHAR(200),
            val VARCHAR(200),
            playerId VARCHAR(200),
            matchId VARCHAR(200),
            PRIMARY KEY (id)
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
                all_data.append([parts1, parts2,parts3,parts4,parts5,parts6,parts7,parts8,parts9,parts10,parts11,parts12,parts13]) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO stats_match (namePlayer, team, pts, reb, ast, min, fgm, fga, `2pm`, `2pa`, `3pm`, `3pa`, ftm) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
            print("SQL query:", sql) # Print the SQL query
        except mysql.connector.Error as error:
            print
            db.rollback()
            error_count += 1
            errors.append(row)
            print("Error message:", error)
        finally:
            cursor.close()
            
    print(f"Total Successes: {success_count}, Total Errors: {error_count}")

if __name__ == '__main__':
    create_table()
        
    csv_files = glob.glob('csv/basketball/summary/*.csv')
    all_data = read_csv_files(csv_files)    
    # Close the database connection
    db.close()
