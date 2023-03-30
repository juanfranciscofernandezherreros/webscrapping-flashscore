import asyncio
import csv
import sys
from pyppeteer import launch

async def main(url):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)    
    
    # Get all elements with the class name "stat__homeValue"
    elementsHome = await page.querySelectorAll('.stat__homeValue')
    
    # Extract the text content of each element
    texts = []
    for element in elementsHome:
        text = await page.evaluate('(element) => element.textContent', element)
        texts.append(text)

    # Get all elements with the class name "stat__awayValue"
    elementsAway = await page.querySelectorAll('.stat__awayValue')
    
    # Extract the text content of each element
    away = []
    for element in elementsAway:
        text = await page.evaluate('(element) => element.textContent', element)
        away.append(text)

    # Get all elements with the class name "stat__categoryName"
    elementsName = await page.querySelectorAll('.stat__categoryName')
    
    # Extract the text content of each element
    name = []
    for element in elementsName:
        text = await page.evaluate('(element) => element.textContent', element)
        name.append(text)

    # Create a bidimensional array by zipping the three arrays together
    stats = list(zip(name, texts, away))

    # Write the bidimensional array to a CSV file
    with open('stats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Home', 'Away'])
        writer.writerows(stats)

    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
