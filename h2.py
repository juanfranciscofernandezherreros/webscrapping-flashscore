import asyncio
from pyppeteer import launch
import os
import csv

async def main():
    
    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "quarters"
    urls_folder = os.path.join(basketball_folder, "pointByPoint")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)
    
    result_array = []
    for i in range(2, 30):
        xpath = f'//*[@id="detail"]/div[9]/div[{i}]/div[1]'
        xpath1 = f'//*[@id="detail"]/div[9]/div[{i}]/div[2]/div[1]'
        xpath2 = f'//*[@id="detail"]/div[9]/div[{i}]/div[2]/div[2]'
        xpath3 = f'//*[@id="detail"]/div[9]/div[{i}]/div[3]'

        element = await page.xpath(xpath)
        element1 = await page.xpath(xpath1)
        element2 = await page.xpath(xpath2)
        element3 = await page.xpath(xpath3)

        text = await element[0].getProperty('textContent')
        text1 = await element1[0].getProperty('textContent')
        text2 = await element2[0].getProperty('textContent')
        text3 = await element3[0].getProperty('textContent')

        text = await text.jsonValue()
        text1 = await text1.jsonValue()
        text2 = await text2.jsonValue()
        text3 = await text3.jsonValue()

        row = []
        if text.strip() != "":
            row.append(text)
        else:
            row.append("-")
        if text1.strip() != "":
            row.append(text1)
        else:
            row.append("-")
        if text2.strip() != "":
            row.append(text2)
        else:
            row.append("-")
        if text3.strip() != "":
            row.append(text3)
        else:
            row.append("-")
        
        result_array.append(row)
    
    url_parts = url.split("/")
    match_id = url_parts[8]
    match_type = url_parts[6]
    match_number = url_parts[4]
    print(match_id)
    print(match_type)
    print(match_number)

    with open(f"csv/basketball/pointByPoint/pointByPoint_{match_id}_{match_number}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Home', 'Away', 'Time'])
        writer.writerows(result_array)

    
    await browser.close()

url = 'https://www.flashscore.com/match/CbOSqht1/#/match-summary/point-by-point/0'
asyncio.get_event_loop().run_until_complete(main())
