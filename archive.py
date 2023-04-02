import asyncio
import csv
import sys
from pyppeteer import launch
import os
import asyncio
import re

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

    team_urls = []
    other_urls = []

    for url in hrefs:
        if 'team' in url:
            team_urls.append(url)
        else:
            other_urls.append(url)

    print("Team URLs:")
    print(team_urls)

    print("Other URLs:")
    url_parts = other_urls[0]
    # Split the URL and extract the required portion
    required_portion = url_parts.split("/")[4:]

    # Replace "/" with "_" in the required portion
    required_portion = "_".join(required_portion)
    
    # Define function to extract team name and team ID from URL
def extract_team_info(url):
    parts = url.split('/')
    team_name = parts[4]
    team_id = parts[5]
    return team_name, team_id
    
    # Export team URLs to CSV
    with open(os.path.join(teams_folder, required_portion+'team_urls.csv'), mode='w', newline='') as file:
        writer = csv.writer(file)
        for url in team_urls:
            
            writer.writerow([url])

    # Export other URLs to CSV
    with open(os.path.join(season_folder, required_portion+'season_urls.csv'), mode='w', newline='') as file:
        writer = csv.writer(file)
        for url in other_urls:
            writer.writerow([url])

    await browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))

