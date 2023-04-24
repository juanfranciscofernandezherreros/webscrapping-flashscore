import asyncio
import csv
import os
from pyppeteer import launch

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
    # Check if URL contains the word 'basketball'
    if 'basketball' in url:
        # Create subfolder 'basketball' if it doesn't exist
        # Make sure the "csv" folder exists
        if not os.path.exists("csv"):
            os.mkdir("csv")
        # Create a subfolder called "basketball"
        basketball_folder = os.path.join("csv", "basketball")
        if not os.path.exists(basketball_folder):
            os.mkdir(basketball_folder)

        # Create a subfolder called "lineups"
        urls_folder = os.path.join(basketball_folder, "urls")
        if not os.path.exists(urls_folder):
            os.mkdir(urls_folder)
            
        csv_path = os.path.join('csv/basketball/urls', filename + '.csv')
    else:
        print("No functionality available for this URL.")
        return
    hrefs = await get_hrefs(url, num_slashes)    
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for href in hrefs:
            writer.writerow([href])

if __name__ == '__main__':
    url = input("Enter the URL: ")
    num_slashes = int(input("Enter the number of slashes: "))
    filename = input("Enter the filename: ")
    asyncio.run(export_to_csv(url, num_slashes, filename))
