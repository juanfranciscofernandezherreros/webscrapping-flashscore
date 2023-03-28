import csv
import mysql.connector

# Connect to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="user_bigdataetl",
    password="password_bigdataetl",
    database="bigdataetl"
)

# Prepare SQL statement
sql = "INSERT INTO matchs (EventTimeUTC, EventTime, HomeTeam, AwayTeam, Quarter1Home, Quarter2Home, Quarter3Home, Quarter4Home, OvertimeHome, Quarter1Away, Quarter2Away, Quarter3Away, Quarter4Away, OvertimeAway) \
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Open CSV file
with open('data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    next(reader) # Skip header row
    
    # Iterate through rows and insert into database
    for row in reader:
        values = tuple(row)
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

# Close database connection
db.close()
