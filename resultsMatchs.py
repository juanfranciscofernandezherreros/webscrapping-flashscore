import argparse
import mysql.connector
import playerStatsMatchsSummary
import playerStatsQuarters
import asyncio
import datetime
import lineups
import pointByPoints
import archive

async def main(second_part):    
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('second_part', type=str, help='second part of the match URL')
    args = parser.parse_args()

    asyncio.run(main(args.second_part))
