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
        WHERE table_name = 'teams'
    """)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute("""
            CREATE TABLE teams (
                id BIGINT NOT NULL AUTO_INCREMENT,
                team_name VARCHAR(200),
                team_id VARCHAR(200) UNIQUE,	
                PRIMARY KEY (id)
            );
        """)
    
    cursor.close()


def read_csv_files(csv_files):
    all_data = []
    
    for file in csv_files:
        print("File: " + file)
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader) # Skip header row
            for row in reader:                
                # The team name and ID are the 4th and 5th elements of the parts list respectively
                team_name = row[0]
                team_id = row[1]
                print("Team Name: ", team_name)
                print("Team ID: ", team_id)
                all_data.append((team_name,team_id)) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO teams (team_name, team_id) \
    VALUES (%s, %s)"
    
    # Create arrays to store successes and errors
    success_count = 0
    error_count = 0
    successes = []
    errors = []
           
    for row in all_data:
        print("Row: " + row[0])
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

    db.close()

if __name__ == '__main__':
    create_table()
    csv_files = glob.glob('csv/basketball/teams/*.csv')
    all_data = read_csv_files(csv_files)
