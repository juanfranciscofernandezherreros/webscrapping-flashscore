import asyncio
import csv
from pyppeteer import launch
from datetime import datetime
from urllib.parse import urlparse
import glob
import os
import mysql.connector
import asyncio
import resultsMatch
import config.database
import sys
import os
import fixtures_init

async def extract_table_data():

    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "lineups"
    urls_folder = os.path.join(basketball_folder, "standings")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

    # Launch a headless Chrome browser
    browser = await launch()
    page = await browser.newPage()

    # Navigate to the webpage containing the table
    await page.goto('https://www.flashscore.com/basketball/spain/acb/standings/')

    # Wait for the table to load
    await page.waitForSelector('.ui-table__row')

    # Extract the table data
    table_data = []
    rows = await page.querySelectorAll('.ui-table__row')

    for row in rows:
        cell_href = await row.querySelectorEval('a', 'a => a.href')  # get href from the first link in the row
        cells = await row.querySelectorAll('.table__cell--participant, .table__cell--value')
        row_data = []
        for cell in cells:
            cell_text = await page.evaluate('(element) => element.textContent', cell)
            row_data.append(cell_text.strip())
          # Split cell_href into ID and team name
        url_parts = urlparse(cell_href)
        path_parts = url_parts.path.split('/')
        team_name = path_parts[-3]
        team_id = path_parts[-2]
        # Append ID and team name to row_data
        row_data.append(team_id)
        row_data.append(team_name)
        table_data.append(row_data)
     # Export table data to CSV file
    with open('csv/basketball/standings/standings', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the headers to the CSV file
        headers = ['name_team','match_games', 'wins', 'loses', 'totalPoints','teamId','playerId']
        writer.writerow(headers)
        for row in table_data:
            writer.writerow(row)

    # Close the browser
    await browser.close()

    return table_data



if __name__ == '__main__':
    asyncio.run(extract_table_data())
