import asyncio
import csv
import sys
from pyppeteer import launch

#py lineups.py https://www.flashscore.com/match/CbOSqht1/#/match-summary/lineups

async def main(url):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto("https://www.flashscore.com/match/CbOSqht1/#/match-summary/lineups")        
    
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
    
    # Extract the text content of each element and the href attribute value of the "a" element inside each ".lf__participantName" element
    texts = []
    for element in participantName:
        text = await page.evaluate('(element) => element.textContent.trim()', element)
        texts.append(text)    

    print(texts)
    
    ids = []
    links = await page.querySelectorAll('a')
    for link in links:
        href = await page.evaluate('(element) => element.href', link)        
        if href and 'player' in href and href.count('/') == 6:
            split_href = href.split("/")
            result = split_href[-2]
            ids.append(result)
    print(ids)
    
        
    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
