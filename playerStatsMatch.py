import mysql.connector
import playerStatsMatchsSummary
import asyncio

async def main():
    # establish a connection to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )

    # create a cursor object to execute queries
    mycursor = mydb.cursor()

    # execute a SELECT query
    mycursor.execute("SELECT matchId FROM matchs WHERE EventTimeUTC BETWEEN 1679853600 AND 1680170956;")

    # retrieve the query results
    myresult = mycursor.fetchall()

    # print the results
    for row in myresult:
        s = row[0]  # extract the URL string from the first (and only) column of the row
        if s.startswith("g_3_"):
            parts = s.split("_")
            if len(parts) == 3:
                second_part = parts[2]
        await playerStatsMatchsSummary.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/player-statistics/0")

# call the asynchronous function
asyncio.run(main())
