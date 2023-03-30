import asyncio
import csv
import sys
from pyppeteer import launch


async def main(url):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)
    data = []
    hrefs = []
    links = await page.querySelectorAll('a')
    
    #Get all links
    player_links_count = 0
    
    links = await page.querySelectorAll('div.ui-table__body a')
    for link in links:
        href = await page.evaluate('(element) => element.href', link)
        if href and "player" in href:
            print("href" + href)
            player_links_count += 1
            
    print("Total player links: ", player_links_count)
     
    for i in range(1, 15):
        for j in range(1, player_links_count+1):
            link = f'//*[@id="detail"]/div[9]/div/div[2]/div[2]/div[{j}]/a'
            xpath = f'//*[@id="detail"]/div[9]/div/div[2]/div[2]/div[{j}]/div[{i}]'
            element = await page.xpath(xpath)
            namePlayer = await page.xpath(link)
            text = await page.evaluate('(element) => element.textContent', element[0])
            text2 = await page.evaluate('(element) => element.textContent', namePlayer[0])
            href = await page.evaluate('(element) => element.href', namePlayer[0])
            # Extract player ID from the URL
            player_id = href.split('/')[-2]
            # Search for existing player and update data if found
            player_found = False
            for player_data in data:
                if player_data[0] == player_id:
                    player_data[i] = text
                    player_found = True
                    break

            # Add new player if not found
            if not player_found:
                player_data = [player_id, text2, href] + [''] * 12
                player_data[i+2] = text
                data.append(player_data)

    # Write data to CSV file
    match_id = url.split("/")[4]
    with open(f'match_data_summary_{match_id}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Name', 'Link', 'Stat1', 'Stat2', 'Stat3', 'Stat4', 'Stat5', 'Stat6', 'Stat7', 'Stat8', 'Stat9', 'Stat10', 'Stat11', 'Stat12', 'Stat13', 'Stat14'])
        for player_data in data:
            writer.writerow(player_data)

    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
