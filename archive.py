import asyncio
import csv
import sys
from pyppeteer import launch
import os
import asyncio
import re

# Define function to extract team name and team ID from URL
def extract_team_info(url):
    parts = url.split('/')
    team_name = parts[4]
    team_id = parts[5]
    return team_name, team_id

async def main(url):
    
    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "teams"
    teams_folder = os.path.join(basketball_folder, "teams")
    if not os.path.exists(teams_folder):
        os.mkdir(teams_folder)
        
    # Create a subfolder called "season"
    season_folder = os.path.join(basketball_folder, "season")
    if not os.path.exists(season_folder):
        os.mkdir(season_folder)    

    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)

    hrefs = await page.evaluate('''() => {
        const elements = Array.from(document.querySelectorAll(".archive a"));
        return elements.map(element => element.href.trim());
    }''')
        
    new_hrefs = []
    new_hrefs1 = []
    for href in hrefs[1:]:
        if "team" not in href:
            new_hrefs.append(href)
        else:
            new_hrefs1.append(href)
    
    for h1 in new_hrefs:
        print(h1)
    for h2 in new_hrefs1:
        print(h2)
    await browser.close()
        
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
