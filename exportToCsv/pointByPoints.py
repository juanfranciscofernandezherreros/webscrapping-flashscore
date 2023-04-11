import asyncio
import csv
import sys
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

    # Create a subfolder called "pointByPoint"
    urls_folder = os.path.join(basketball_folder, "pointByPoint")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)


    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)        
    
    # scrape the score information
    scores = await page.evaluate('''() => {
        const rows = Array.from(document.querySelectorAll('.matchHistoryRow'))
        return rows.map(row => ({
            homeScore: row.querySelector('.matchHistoryRow__scoreBox .matchHistoryRow__score:first-child').textContent.trim(),
            awayScore: row.querySelector('.matchHistoryRow__scoreBox .matchHistoryRow__score:last-child').textContent.trim(),
            homeAdvantage: row.querySelector('.matchHistoryRow__ahead.matchHistoryRow__home')?.textContent.trim(),
            awayAdvantage: row.querySelector('.matchHistoryRow__ahead.matchHistoryRow__away')?.textContent.trim(),
        }))
    }''')
    
    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
