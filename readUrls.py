import asyncio
import csv
from pyppeteer import launch
import readCsvUrls
async def get_hrefs(url, num_slashes):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    print("URL" + url)
    newUrlsToAdd = []
    # Get all "a" tags on the page and their href attributes
    hrefs = await page.querySelectorAllEval('a', 'nodes => Array.from(nodes, n => n.href)')
    hrefs = set(hrefs)  # convert to a set to remove duplicates
    # Filter hrefs to only include those with a specific pattern
    filtered_hrefs = set(filter(lambda x: 'basketball' in x and x.count('/') == num_slashes, hrefs))        
    await browser.close()
    return filtered_hrefs
async def export_to_csv(url, num_slashes, filename):
    hrefs = await get_hrefs(url, num_slashes)    
    readCsvUrls.main();
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for href in hrefs:
            writer.writerow([href])

if __name__ == '__main__':
    url = 'https://www.flashscore.com/basketball/spain'
    num_slashes = 6
    filename = 'newUrls.csv'
    asyncio.run(export_to_csv(url, num_slashes, filename))
