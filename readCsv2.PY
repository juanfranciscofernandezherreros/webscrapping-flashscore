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
sql = "INSERT INTO matchs (EventTimeUTC, EventTime, HomeTeam, AwayTeam, Quarter1Home, Quarter2Home, Quarter3Home, Quarter4Home, OvertimeHome, Quarter1Away, Quarter2Away, Quarter3Away, Quarter4Away, OvertimeAway) \
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Create arrays to store successes and errors
successes = []
errors = []

# Open CSV file
with open('data.csv', newline='') as csvfile:
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
            
    #Get list of emails to send
    # Create a cursor object
    mycursor = db.cursor()

    # Generate the SELECT statement
    select_query = "SELECT email,hasActive FROM sendersMail"

    # Execute the SELECT query
    mycursor.execute(select_query)

    # Get the results and insert into an array
    results = []
    for row in mycursor.fetchall():
        if row[1] == "Y":
            email = row[0]
            results.append(email)
            
    print(results)            
    # Close database connection
    
db.close()

# Export data to CSV files
with open('successes.csv', 'w', newline='') as success_file:
    success_writer = csv.writer(success_file, delimiter=';', quotechar='"')
    success_writer.writerow(['Event Time UTC', 'Event Time', 'Home Team', 'Away Team', '1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter', 'Overtime Home', '1st Quarter Away', '2nd Quarter Away', '3rd Quarter Away', '4th Quarter Away', 'Overtime Away'])
    success_writer.writerows(successes)

with open('errors.csv', 'w', newline='') as error_file:
    error_writer = csv.writer(error_file, delimiter=';', quotechar='"')
    error_writer.writerow(['Event Time UTC', 'Event Time', 'Home Team', 'Away Team', '1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter', 'Overtime Home', '1st Quarter Away', '2nd Quarter Away', '3rd Quarter Away', '4th Quarter Away', 'Overtime Away'])
    error_writer.writerows(errors)

subject = "Email Subject"
body = "This is the body of the text message /// SUCCESS WRITING " + str(successes) + "/// ERROR INSERTING" + str(errors)
sender = "juanfranciscofernandezherreros@gmail.com"
recipients = results
password = "*"

sendEmail.send_email(subject, body, sender, recipients, password)