import asyncio
import csv
import sys
from pyppeteer import launch

#py lineups.py https://www.flashscore.com/match/CbOSqht1/#/match-summary/lineups

async def main(url):
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

    # Get all elements with the class name "lf__participantNumber"
    participantName = await page.querySelectorAll('.lf__participantName')
    
    # Extract the text content of each element and the href attribute value of the "a" element inside each ".lf__participantName" element
    texts = []
    ids = []
    links = await page.querySelectorAll('a')
    for element in participantName:
        text = await page.evaluate('(element) => element.textContent.trim()', element)
        texts.append(text)    
        href = await element.getProperty('href')
        href = await href.jsonValue()
        if href and 'player' in href and href.count('/') == 6:
            split_href = href.split("/")
            result = split_href[-2]
            ids.append(result)

    # Combine number, texts, and ids into a bidimensional array
    lineup_data = list(zip(number, texts, ids))
    match_id = url.split("/")[-2]
    print("MatchId" + match_id)
    # Write lineup_data to a CSV file
    with open('lineups'+match_id+'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lineup_data)
        
    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
