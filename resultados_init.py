import mysql.connector
import asyncio
import resultsMatch
import config.database
import sys
import os 

async def main(url, country, competition):
    # establish a connection to the MySQL database
    mydb = config.database.conectar()

    # create a cursor object to execute queries
    mycursor = mydb.cursor()

    # execute a SELECT query
    query = "SELECT DISTINCT urls FROM urls WHERE urls LIKE '%{}%' AND urls LIKE '%{}%' AND urls LIKE '%{}%'".format(url, country, competition)
    mycursor.execute(query)

    # retrieve the query results
    myresult = mycursor.fetchall()

    if 'results' in url and len(myresult) > 0:
        print("URL: " + url)
        # print the results
        for row in myresult:
            url = row[0]  # extract the URL string from the first (and only) column of the row
            print("URL: " + url)
            await resultsMatch.main(url)
    else:
        print("URL does not match criteria:", url)

if __name__ == '__main__':
    url = sys.argv[1]
    countries = sys.argv[2]
    competition = sys.argv[3]
    asyncio.run(main(url,countries,competition))
    