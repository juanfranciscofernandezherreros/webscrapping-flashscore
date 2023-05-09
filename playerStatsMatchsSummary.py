import csv
import sys
import asyncio
from pyppeteer import launch
import mysql.connector
import asyncio
import config.database
import sys
import os
import re

async def main(url):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)

    tabs = await page.querySelectorAll('a.tabs__tab')

    print("SUMMARY", url)
    game_id = url.split("/")[-4]

    for tab in tabs:
        tab_text = await page.evaluate('(element) => element.textContent', tab)
        print("TABS",tab_text)
        href = await tab.getProperty('href')
        href_val = await href.jsonValue()
        print("href:", href_val)
        if tab_text == "Summary":
            print("Summary")
            summary_data = await _get_summary_data(page)
            await _write_summary_to_csv(game_id, summary_data)     
        # Navigate to the player statistics page
        if tab_text == "Player Statistics":
                print("Player Statistics")
                href = await tab.getProperty('href')
                href_val = await href.jsonValue()
                url = href_val + "/0"                
                print("Navigating to:", url)
                await page.goto(url)     
                await asyncio.sleep(5)                                                 
        # Navigate to the player statistics page
        if tab_text == "Stats":
                print("MatchStatistics")
                href = await tab.getProperty('href')
                href_val = await href.jsonValue()
                url = href_val + "/0"
                print("Navigating to:", url)
                await page.goto(url)            
                subLinks = await extract_hrefs(url,"match-statistics")
                await asyncio.sleep(5) 
                for link in subLinks:
                    print("SubLink" , link) 
                    if link.count('/') == 8:
                        print('The URL contains exactly 8 slashes.')
                        await page.goto(link)  
                        await asyncio.sleep(5) 
                        data = await _get_match_stats_data(page)
                        number = re.search(r'/(\d+)$', link).group(1)
                        if data:
                            data_dicts = [dict(zip(['local', 'stat', 'visitor','quarter', 'game_id'], d)) for d in data]
                            filename = f"csv/basketball/matchStatistics/{game_id}_{number}_matchStatistics.csv"
                            try:
                                # Check if directory exists and create it if it doesn't
                                os.makedirs(os.path.dirname(filename), exist_ok=True)
                                # Write the data to CSV file
                                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                                    fieldnames = ['local', 'stat', 'visitor','quarter', 'game_id']
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writeheader()
                                    for d in data_dicts:
                                        d['quarter'] = number
                                        d['game_id'] = game_id
                                        writer.writerow(d)
                                print(f"CSV file {filename} has been generated successfully.")
                            except Exception as e:
                                print(f"Error generating CSV file {filename}: {e}")
                        else:
                            print("No data retrieved from the page.")                              
        # Navigate to the player statistics page
        if tab_text == "Lineups":
            print("Lineups")
            href = await tab.getProperty('href')
            href_val = await href.jsonValue()
            url = href_val
            print("Navigating to:", url)
            await page.goto(url)            
            await asyncio.sleep(5) 
            # Get all cell elements and their text
            data = await _get_lineUps_data(page)
            if data:
                filename = f"csv/basketball/lineups/{game_id}_lineups.csv"
                # Escribir los datos en un archivo CSV
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['number', 'flag', 'name', 'player_id', 'player_code', 'game_id']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for d in data:
                        d['game_id'] = game_id
                        writer.writerow(d)
            else:
                print("No data retrieved from the page.")
        # Navigate to the player statistics page
        if tab_text == "Match History":
            print("Match History")
            href = await tab.getProperty('href')
            href_val = await href.jsonValue()            
            url = href_val + "/0"
            print("Navigating to:", url)
            await page.goto(url)            
            subLinks1 = await extract_hrefs(url,"point-by-point")
            await asyncio.sleep(5)
            for link in subLinks1:
                print("SubLink" , link)            
                if link.count('/') == 8:
                        print('The URL contains exactly 8 slashes.')
                        await page.goto(link)  
                        await asyncio.sleep(5) 
                        data = await _get_matchHistory_data(page)
                        if data:
                            number = re.search(r'/(\d+)$', link).group(1)
                            filename = f"csv/basketball/pointByPoint/{game_id}_{number}_pointByPoint.csv"                        
                            try:
                                # Check if directory exists and create it if it doesn't
                                os.makedirs(os.path.dirname(filename), exist_ok=True)
                                # Write the data to CSV file
                                with open(filename, 'w', newline='') as csvfile:
                                    writer = csv.writer(csvfile)
                                    writer.writerow(['Match', 'Scores','Game_Id','Quarter'])
                                    for i, score in enumerate(data):
                                        writer.writerow([i+1, score,game_id,number])
                                print(f"CSV file {filename} has been generated successfully.")
                            except Exception as e:
                                print(f"Error generating CSV file {filename}: {e}")
                        else:
                            print("No data retrieved from the page.")
    await browser.close()

async def _get_summary_data(page):
    total_home = await page.querySelector('.smh__part.smh__score.smh__home.smh__part--current')
    total_away = await page.querySelector('.smh__part.smh__score.smh__away.smh__part--current')
    total__home = await page.evaluate('(element) => element.textContent', total_home)
    total__away = await page.evaluate('(element) => element.textContent', total_away)

    quarters = ['1', '2', '3', '4', '5']
    quarter_scores = []

    for q in quarters:
        quarter_local = await page.querySelector(f'.smh__part.smh__home.smh__part--{q}')
        quarter_away = await page.querySelector(f'.smh__part.smh__away.smh__part--{q}')
        quarter_local_text = await page.evaluate('(element) => element.textContent', quarter_local)
        quarter_away_text = await page.evaluate('(element) => element.textContent', quarter_away)
        quarter_scores.append(quarter_local_text)
        quarter_scores.append(quarter_away_text)

    return {
        "total_home": total__home,
        "total_away": total__away,
        "quarter_scores": quarter_scores
    }

async def _get_player_stats_data(page):
    row_selector = '.playerStatsTable__row'
    row_elements = await page.querySelectorAll(row_selector)
    data = []

    for row_element in row_elements:
        # Extract the text content of each cell element in the row
        row_data = await page.evaluate('''(row) => {
            const cells = row.querySelectorAll('.playerStatsTable__cell');
            const rowData = [];
            for (const cell of cells) {
                rowData.push(cell.textContent.trim());
            }
            return rowData;
        }''', row_element)

        # Extract the href value from the first cell element in the row
        href_element = await row_element.querySelector('.playerStatsTable__participantCell')
        href = await href_element.getProperty('href')
        href_val = await href.jsonValue()
        href_parts = href_val.split('/')
        player_name = href_parts[-2]
        player_id = href_parts[-1]
        row_data.insert(1, player_name)  # Insert the href value as the second element of the row
        row_data.insert(2, player_id)  # Insert the href value as the third element of the row
        data.append(row_data)  # Append the row data to the list of data

    return data

async def _get_match_stats_data(page):
    # Use page.querySelectorAll to extract all elements with the class 'stat__category'
    elements = await page.querySelectorAll('.stat__category')
    data = []
    
    # Lo
    # op over the elements and extract the text content of each group of elements
    for element in elements:
        # Use element.querySelectorAll to extract the three matching elements
        value_elements = await element.querySelectorAll('.stat__homeValue, .stat__categoryName, .stat__awayValue')
        
        # Extract the text content of each element and add it to the data list
        values = []
        for value_element in value_elements:
            value = await page.evaluate('(value_element) => value_element.textContent', value_element)
            values.append(value)
        data.append(values)
    
    return data

async def _get_lineUps_data(page):
    print("LineUps")
    data = []
    elements = await page.querySelectorAll('.lf__participantNumber, .lf__participantFlag, .lf__participantName')
    for i in range(0, len(elements), 3):
        number, flag, name_elem = elements[i:i+3]
        number_text = await page.evaluate('(element) => element.textContent', number)
        flag_title = await page.evaluate('(element) => element.getAttribute("title")', flag)
        name_text = await page.evaluate('(element) => element.textContent', name_elem)
        name_href = await page.evaluate('(element) => element.getAttribute("href")', name_elem)
        player_id, player_code = name_href.split('/')[2:4]
        data.append({'number': number_text, 'flag': flag_title, 'name': name_text, 'player_id': player_id, 'player_code': player_code})
    return data

async def _get_matchHistory_data(page):
    game_id = url.split("/")[-4]
    # Wait for the selector to appear on the page
    await page.waitForSelector('.matchHistoryRow__score')
    # Get a list of all matching elements
    elements = await page.querySelectorAll('.matchHistoryRow__score')
    # Initialize an empty array to store the extracted texts
    texts = []
    # Loop through each element and extract the text
    for i, element in enumerate(elements):
        text = await page.evaluate('(element) => element.textContent', element)
        if i % 2 == 0:
            # If i is even, append the text to the texts array
            texts.append(text)
        else:
            # If i is odd, concatenate the previous element with the current element
            concatenated_text = texts.pop() + '/' + text
            # Append the concatenated text to the texts array
            texts.append(concatenated_text)
    # Return the texts array
    return texts

async def _write_summary_to_csv(game_id, summary_data):
    filename = f"csv/basketball/summary/{game_id}_summary.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Game ID", "Total Home", "Total Away", "Q1 Local", "Q1 Away", "Q2 Local", "Q2 Away", "Q3 Local", "Q3 Away", "Q4 Local", "Q4 Away", "Q5 Local", "Q5 Away"])
        writer.writerow([game_id, summary_data["total_home"], summary_data["total_away"]] + summary_data["quarter_scores"])

async def _write_playerStatistics_to_csv(game_id, player_stats_data,numero):
    filename = f"csv/basketball/playerStatistics/{game_id}_{numero}_playerStatistics.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Player Name", "Player ID", "Team", "Min", "Pts", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "PF", "+/-", "Game ID"])
        for row in player_stats_data:
            row.append(game_id)  # Add the Game ID to the row data
            writer.writerow(row)

async def extract_hrefs(url ,frase):
    """Extract hrefs from a webpage"""
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    hrefs = await page.evaluate('''() => {
        return [...document.querySelectorAll('a')].map(elem => elem.href);
    }''')
    filtered_hrefs = set(filter(lambda x: frase in x, hrefs))
    await browser.close()
    return filtered_hrefs

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
