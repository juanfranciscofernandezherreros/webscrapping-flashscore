import asyncio
import csv
import sys
from pyppeteer import launch
import os
import asyncio

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

    hrefs = await page.evaluate('''() => {
        const hrefs = [];
        const elements = document.querySelectorAll("a");
        for (let element of elements) {
            hrefs.push(element.href);
        }
        return hrefs;
    }''')
    
    for url in hrefs:
        if 'team' in url:
            url_parts = url.split('/')
            team_id = url_parts[-3]
            team_name = url_parts[-2]

            print("Team ID:", team_id)
            print("Team Name:", team_name)

    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))