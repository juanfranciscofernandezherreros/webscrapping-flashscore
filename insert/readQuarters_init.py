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
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'quarters'
    """)
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        cursor.execute("""
            CREATE TABLE quarters (
                id BIGINT NOT NULL AUTO_INCREMENT,
                attribute VARCHAR(50),
                homePercentage VARCHAR(50),
                visitorPercentage VARCHAR(50),
                matchId VARCHAR(50),
                quarter VARCHAR(50),
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
                # Remove % symbol only if there is one in the string
                if parts2.count('%') == 1:
                    parts2 = parts2.replace("%", "") + '%'
                else:
                    parts2 = parts2 + '%'
                if parts3.count('%') == 1:
                    parts3 = parts3.replace("%", "") + '%'
                else:
                    parts3 = parts3 + '%'
                parts4 = row[3]
                parts5 = row[4]

                all_data.append([parts1, parts2, parts3, parts4,parts5]) # Add row to all_data                
    
    # Prepare SQL statement
    sql = "INSERT INTO quarters (attribute, homePercentage, visitorPercentage, matchId, quarter) VALUES (%s, %s, %s, %s, %s)"
    
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
    csv_files = glob.glob('../csv/basketball/quarters/*.csv')
    all_data = read_csv_files(csv_files)
    
    # Close the database connection
    db.close()
