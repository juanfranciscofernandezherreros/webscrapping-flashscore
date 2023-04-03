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

    # Create a subfolder called "lineups"
    urls_folder = os.path.join(basketball_folder, "lineups")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)


    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)        
    
    # Get all elements with the class name "lf__participantNumber"
    participantNumber = await page.querySelectorAll('.lf__participantNumber')
    
    # Extract the text content of each element
    number = []
    for element in participantNumber:
        text = await page.evaluate('(element) => element.textContent', element)
        number.append(text)    

    print(number)
    
    # Get all elements with the class name "lf__participantNumber"
    participantName = await page.querySelectorAll('.lf__participantName')
    
    # Get all links and extract the "href" attribute value for the player pages
    ids = []
    links = await page.querySelectorAll('a')
    for link in links:
        href = await page.evaluate('(element) => element.href', link)        
        if href and 'player' in href and href.count('/') == 6:
            split_href = href.split("/")
            result = split_href[-2]
            ids.append(result)
    print(ids)

    # Extract the text content of each ".lf__participantName" element
    texts = []
    for element in participantName:
        text = await page.evaluate('(element) => element.textContent.trim()', element)
        texts.append(text)    

    print(texts)
    
    # Combine the arrays into a bidimensional array
    results = []
    for i in range(len(number)):
        item = [number[i], texts[i], ids[i]]
        if i < 10:
            item.append('Starter')
        else:
            item.append('Substitute')
        results.append(item)         
    
    url_parts = url.split("/")
    match_id = url_parts[4]
    print(match_id)
    
    # Write data to CSV file
    with open(f"csv/basketball/lineups/lineups_{match_id}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['numberPlayer', 'namePlayer', 'playerId', 'Starter', 'MatchId'])
        for row in results:
            row.insert(4, match_id)
            writer.writerow(row)
    
    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
