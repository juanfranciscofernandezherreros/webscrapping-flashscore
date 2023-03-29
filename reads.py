import csv
import mysql.connector
import sendEmail

def main(my_array):
    for item in my_array:
        print("Item" + item)
    # Connect to the MySQL server
    db = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )

    # Prepare SQL statement
    sql = "INSERT INTO urls (urls,country,isOpened) \
    VALUES (%s,'F')"
    # Create arrays to store successes and errors
    successes = []
    errors = []
    
    # Loop through my_array and insert data into MySQL
    for item in str(my_array):
        try:
            # Execute the SQL statement
            val = (item)
            mycursor = db.cursor()
            mycursor.execute(sql, val)
            db.commit()

            # Add success to successes array
            successes.append(item)

        except mysql.connector.Error as error:
            # Add error to errors array
            errors.append(item)
            print("Failed to insert record into MySQL table: {}".format(error)) 

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

    # Send email
    subject = "Email Subject"
    body = "This is the body of the text message /// SUCCESS WRITING " + str(successes) + "/// ERROR INSERTING" + str(errors)
    sender = "juanfranciscofernandezherreros@gmail.com"
    recipients = results
    password = "*"       
    sendEmail.send_email(subject,body,sender,recipients,password)
    db.close()
        
if __name__ == "__main__":
    sendArray = []
    main(sendArray)
