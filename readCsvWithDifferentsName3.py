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

def read_csv_files(csv_files):
    all_data = []
    
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
    successes = []
    errors = []
           
    for row in all_data:
        print("Row" + row[0])
        values = tuple(row)
        cursor = db.cursor()
        
        try:
            cursor.execute(sql, values)
            db.commit()
            successes.append(row)
            
        except mysql.connector.Error as error:
            db.rollback()
            errors.append(row)
            print("Error inserting row {}: {}".format(row, error))

        finally:
            cursor.close()
    
if __name__ == '__main__':
    csv_files = glob.glob('spain_acb_*.csv')
    all_data = read_csv_files(csv_files)
