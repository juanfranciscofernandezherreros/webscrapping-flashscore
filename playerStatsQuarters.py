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

    # Create a subfolder called "quarters"
    urls_folder = os.path.join(basketball_folder, "quarters")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

    
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
    
    number = url.split("/")[-1]
    print("Quarter" + number)
    match_id = url.split("/")[-5]
    print("MatchId" + match_id)
    with open(f"csv/basketball/quarters/quarters_{number}_{match_id}.csv", 'w', newline='') as file:
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
