import asyncio
import os
import csv
from pyppeteer import launch

async def main(url):
    # rest of the code
    
    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "pointByPoint"
    point_by_point_folder = os.path.join(basketball_folder, "pointByPoint")
    if not os.path.exists(point_by_point_folder):
        os.mkdir(point_by_point_folder)

    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)
    
    
    
    await browser.close()

url = 'https://www.flashscore.com/match/CbOSqht1/#/match-summary/point-by-point/0'
asyncio.get_event_loop().run_until_complete(main(url))
