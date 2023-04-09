import argparse
import mysql.connector
import playerStatsMatchsSummary
import playerStatsQuarters
import asyncio
import datetime
import lineups
import pointByPoints
import h2
import archive
from config import DATABASE_CONFIG

async def main(second_part):
    # establish a connection to the MySQL database
    mydb = mysql.connector.connect(**DATABASE_CONFIG)
    
    await playerStatsMatchsSummary.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/player-statistics/0")
    await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/0")
    await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/1")
    await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/2")
    await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/3")
    await playerStatsQuarters.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/match-statistics/4")
    await lineups.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/lineups")
    await h2.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/0")
    await h2.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/1")
    await h2.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/2")
    await h2.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/3")
    await h2.main("https://www.flashscore.com/match/"+second_part+"/#/match-summary/point-by-point/4")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('second_part', type=str, help='second part of the match URL')
    args = parser.parse_args()

    asyncio.run(main(args.second_part))
