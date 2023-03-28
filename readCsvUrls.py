import csv
import mysql.connector
import sendEmail

# Connect to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="user_bigdataetl",
    password="password_bigdataetl",
    database="bigdataetl"
)

# Prepare SQL statement
sql = "INSERT INTO urls (urls) \
VALUES (%s)"

# Create arrays to store successes and errors
successes = []
errors = []

# Open CSV file
with open('hrefs.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    next(reader) # Skip header row
    
    # Iterate through rows and insert into database
    for row in reader:
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
    
db.close()