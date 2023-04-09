import datetime
import mysql.connector
from config import DATABASE_CONFIG
import asyncio
import resultsMatchs
import os
async def main():

    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "summary"
    urls_folder = os.path.join(basketball_folder, "summary")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

if __name__ == '__main__':
    asyncio.run(main())
