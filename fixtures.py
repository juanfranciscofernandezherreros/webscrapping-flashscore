import sys
import re
import asyncio
import csv
from pyppeteer import launch
import os

async def main(url):
    
    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "fixtures"
    urls_folder = os.path.join(basketball_folder, "fixtures")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)


    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    # Get all elements that start with id #g_3_
    elements = await page.querySelectorAll('[id^="g_3_"]')

    # Initialize an empty two-dimensional array to store the match data
    matches = []

    # Loop through each element and get its text content and ID
    for element in elements:
        text_content = await page.evaluate('(element) => element.innerText', element)
        match_id = await page.evaluate('(element) => element.id', element)
        home_team_logo_src = await page.evaluate('(element) => element.querySelector(".event__logo--home").getAttribute("src")', element)
        away_team_logo_src = await page.evaluate('(element) => element.querySelector(".event__logo--away").getAttribute("src")', element)

        # Split the text content into an array using line breaks as the delimiter
        match_data = text_content.split('\n')

        # Add the match ID and logos to the beginning of the match data array
        match_data.insert(0, match_id)
        match_data.insert(2, home_team_logo_src)
        match_data.insert(3, away_team_logo_src)

        # Add the match data into the matches array
        matches.append(match_data)

    await browser.close()

    # Extract the relevant parts of the URL to generate the CSV filename
    pattern = r'https://www\.flashscore\.com/basketball/spain/acb/fixtures/'
    csv_filename = re.sub(pattern, '', url)
    csv_filename = re.sub(r'/$', '', csv_filename)
    csv_filename = re.sub(r'/', '_', csv_filename)
    csv_filename = csv_filename + '.csv'
    csv_filename = 'spain_acb_fixtures' + csv_filename

    # Export the matches array to a CSV file with headers
    with open(f"csv/basketball/fixtures/{csv_filename}", 'w', newline='') as csvfile:
        fieldnames = ['Match ID', 'Date', 'Home Team Logo', 'Away Team Logo', 'Time', 'Home Team', 'Away Team', 'Score Home', 'Score Away']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fieldnames)
        for match in matches:
            csvwriter.writerow(match)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        asyncio.get_event_loop().run_until_complete(main(url))
    else:
        print('Usage: python script.py <url>')
