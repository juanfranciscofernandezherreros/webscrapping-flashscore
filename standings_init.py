import asyncio
import csv
import sys
from pyppeteer import launch

async def main(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(5)
    # Find all the elements that match the CSS selector
    elements = await page.querySelectorAll('.tableCellParticipant__name')

    # Extract the href attribute value of each element and store it in a list
    new_hrefs1_info = []
    for element in elements:
        link = await (await element.getProperty('href')).jsonValue()
        segments = link.split("/")
        team_id = segments[-2]
        team_name = segments[-3]
        new_hrefs1_info.append({
                "team_name": team_name,
                "team_id": team_id
            })
    
    with open(f"csv/basketball/teams/teams_standings.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['team_name', 'team_id'])
        writer.writeheader()
        for row in new_hrefs1_info:
            writer.writerow(row)

    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python script.py url')
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
