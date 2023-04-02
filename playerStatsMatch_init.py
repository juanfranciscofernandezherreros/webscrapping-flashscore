import mysql.connector
import playerStatsMatchsSummary
import playerStatsQuarters
import asyncio
import datetime
import lineups
import pointByPoints
import h2

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
    
    # Obtener la fecha actual
    date = datetime.date.today()

    # Obtener la fecha en el formato deseado
    formatted_date = date.strftime("%Y,%m,%d")

    print(formatted_date)
    
    # Set the date you're interested in
    year, month, day = map(int, formatted_date.split(","))

    date = datetime.date(year, month, day)  # year, month, day

    # Get the timestamps for 00:01 and 23:59 of that day
    start_timestamp = int(datetime.datetime.combine(date, datetime.time.min).timestamp())
    end_timestamp = int(datetime.datetime.combine(date, datetime.time.max).timestamp())
    
    query = f"SELECT matchId FROM matchs WHERE EventTimeUTC BETWEEN {start_timestamp} AND {end_timestamp};"
    
    print("Query" + query)
    # execute a SELECT query
    mycursor.execute(query)

    # retrieve the query results
    myresult = mycursor.fetchall()

    # print the results
    for row in myresult:
        s = row[0]  # extract the URL string from the first (and only) column of the row
        if s.startswith("g_3_"):
            parts = s.split("_")
            if len(parts) == 3:
                second_part = parts[2]
        #await playerStatsMatchsSummary.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/player-statistics/0")
        #await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/0")
        #await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/1")
        #await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/2")
        #await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/3")
        #await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/4")
        #await lineups.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/lineups")
        #await pointByPoints.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/0")
        await h2.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/0")
asyncio.run(main())
