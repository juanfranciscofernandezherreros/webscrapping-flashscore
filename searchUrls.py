import argparse
import asyncio
import csv
from pyppeteer import launch
#py searchUrls.py https://www.flashscore.com/basketball/
async def main(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    
    hrefs = []
    links = await page.querySelectorAll('a')
    for link in links:
        href = await page.evaluate('(element) => element.href', link)
        if href:
            hrefs.append(href)
    
    await browser.close()
    
    # Write hrefs to a CSV file
    with open('hrefs.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for href in hrefs:
            writer.writerow([href])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract all hrefs from a web page')
    parser.add_argument('url', type=str, help='URL of the web page')
    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(main(args.url))