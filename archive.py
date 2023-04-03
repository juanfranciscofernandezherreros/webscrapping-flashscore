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
        
    # Create a subfolder called "season"
    season_folder = os.path.join(basketball_folder, "archive")
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
    
    new_hrefs_info = []
    for h1 in new_hrefs:
        parts = h1.split("/")
        snippet = "/".join(parts[-3:])
        parts = snippet.split("/")
        name = parts[0]
        name1 = parts[1]
        partes = name1.split("-")
        league = partes[0]
        season = partes[1] + "-" + partes[2]
        new_hrefs_info.append({
                "country": name,
                "league": league,
                "season": season
            })
            
    new_hrefs1_info = []
    for h2 in new_hrefs1:
        parts = h2.split("/")
        team_name = parts[4]
        team_id = parts[5]
        new_hrefs1_info.append({
                "team_name": team_name,
                "team_id": team_id
            })
            
    result = []
    
    for info, info1 in zip(new_hrefs_info, new_hrefs1_info):
        print("Country:", info["country"])
        print("League:", info["league"])
        print("Season:", info["season"])
        print("Team name:", info1["team_name"])
        print("Team ID:", info1["team_id"])
        result.append({
            "Country": info["country"],
            "League": info["league"],
            "Season": info["season"],
            "Team name": info1["team_name"],
            "Team ID": info1["team_id"]
        })
        
    
    parts = url.split('/')
    country = parts[4]

    with open(f"csv/basketball/archive/archive_{country}.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Country', 'League', 'Season', 'Team name', 'Team ID'])
        writer.writeheader()
        for row in result:
            writer.writerow(row)

    
    await browser.close()
        
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
