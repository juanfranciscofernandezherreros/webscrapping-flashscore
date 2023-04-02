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
        print("File: " + file)
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                # Split the row into parts using ';' as a separator
                parts = row[0].split('/')

                # The team name and ID are the 4th and 5th elements of the parts list respectively
                team_name = parts[4]
                team_id = parts[5]

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
    csv_files = glob.glob('csv/basketball/teams/*.csv')
    all_data = read_csv_files(csv_files)
