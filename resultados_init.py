import mysql.connector
import asyncio
from config import DATABASE_CONFIG
import resultsMatch

async def main():
    # establish a connection to the MySQL database
    mydb = mysql.connector.connect(**DATABASE_CONFIG)
    # create a cursor object to execute queries
    mycursor = mydb.cursor()

    # execute a SELECT query
    mycursor.execute("SELECT DISTINCT urls FROM urls WHERE urls LIKE '%results%' AND urls LIKE '%spain%'")

    # retrieve the query results
    myresult = mycursor.fetchall()

    # print the results
    for row in myresult:
        url = row[0]  # extract the URL string from the first (and only) column of the row
        print("URL:"+url)
        await resultsMatch.main(url)
# call the asynchronous function
asyncio.run(main())