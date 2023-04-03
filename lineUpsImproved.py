import asyncio
import csv
import sys
import os
import mysql.connector
from pyppeteer import launch

CSV_FOLDER = "csv"
BASKETBALL_FOLDER = os.path.join(CSV_FOLDER, "basketball")
LINEUPS_FOLDER = os.path.join(BASKETBALL_FOLDER, "lineups")

async def main(url, db_user, db_password, db_host, db_name):
    
    # Create folders if they don't exist
    for folder in [CSV_FOLDER, BASKETBALL_FOLDER, LINEUPS_FOLDER]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    # Launch browser and navigate to URL
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)

    try:
        # Extract player numbers
        player_numbers = []
        participant_number_elements = await page.querySelectorAll('.lf__participantNumber')
        for element in participant_number_elements:
            text = await page.evaluate('(element) => element.textContent', element)
            player_numbers.append(text)
        print(player_numbers)

        # Extract player names and IDs
        player_names = []
        player_ids = []
        participant_name_elements = await page.querySelectorAll('.lf__participantName')
        for element in participant_name_elements:
            text = await page.evaluate('(element) => element.textContent.trim()', element)
            href = await page.evaluate('(element) => element.querySelector("a").href', element)
            if href and 'player' in href and href.count('/') == 6:
                player_id = href.split("/")[-2]
                player_names.append(text)
                player_ids.append(player_id)
        print(player_names)
        print(player_ids)

        # Combine player data into a 2D array
        player_data = []
        for i in range(len(player_numbers)):
            starter_or_substitute = 'Starter' if i < 10 else 'Substitute'
            player_data.append([player_numbers[i], player_names[i], player_ids[i], starter_or_substitute])

        # Write player data to CSV file
        match_id = url.split("/")[-2]
        csv_path = os.path.join(LINEUPS_FOLDER, f"lineups_{match_id}.csv")
        with open(csv_path, 'w', newline
