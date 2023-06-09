import csv
import glob
import mysql.connector

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
        CREATE TABLE IF NOT EXISTS pointByPoints (
            id BIGINT NOT NULL AUTO_INCREMENT,
            actionLocal VARCHAR(200),
            totalPointsLocal VARCHAR(200),
            totalPointsVisitor VARCHAR(200),    
            actionVisitor VARCHAR(200),
            quarter VARCHAR(200),
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
                # Split the row into parts using ';' as a separator
                parts1 = row[0]
                parts2 = row[1]
                parts3 = row[2]
                parts4 = row[3]
                parts5 = row[4]
                parts6 = row[5]


                all_data.append([parts1, parts2, parts3, parts4, parts5, parts6]) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO pointByPoints (actionLocal, totalPointsLocal, totalPointsVisitor, actionVisitor, quarter, matchId ) \
    VALUES (%s, %s, %s, %s, %s, %s)"

    
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
    csv_files = glob.glob('../csv/basketball/pointByPoint/*.csv')
    all_data = read_csv_files(csv_files)
    
    # Close the database connection
    db.close()
