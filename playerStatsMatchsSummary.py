import csv
import sys
import asyncio
from pyppeteer import launch
import mysql.connector
import asyncio
import config.database
import sys
import os

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
                await asyncio.sleep(5)  # Wait for 5 seconds after navigating to the page.            
                # Get all cell elements and their text
                data = await _get_player_stats_data(page)
                await _write_playerStatistics_to_csv(game_id, data)     
        # Navigate to the player statistics page
        if tab_text == "Stats":
                print("Stats")
                href = await tab.getProperty('href')
                href_val = await href.jsonValue()
                url = href_val + "/0"
                print("Navigating to:", url)
                await page.goto(url)            
                await asyncio.sleep(5) 
                # Get all cell elements and their text
                data = await _get_match_stats_data(page)
                await _write_matchStatistics_to_csv(game_id, data)     
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
    
    # Loop over the elements and extract the text content of each group of elements
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


async def _write_summary_to_csv(game_id, summary_data):
    filename = f"csv/basketball/summary/{game_id}_summary.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Game ID", "Total Home", "Total Away", "Q1 Local", "Q1 Away", "Q2 Local", "Q2 Away", "Q3 Local", "Q3 Away", "Q4 Local", "Q4 Away", "Q5 Local", "Q5 Away"])
        writer.writerow([game_id, summary_data["total_home"], summary_data["total_away"]] + summary_data["quarter_scores"])

async def _write_playerStatistics_to_csv(game_id, player_stats_data):
    filename = f"csv/basketball/playerStatistics/{game_id}_playerStatistics.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Player Name", "Player ID", "Team", "Min", "Pts", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "PF", "+/-", "Game ID"])
        for row in player_stats_data:
            row.append(game_id)  # Add the Game ID to the row data
            writer.writerow(row)

async def _write_matchStatistics_to_csv(game_id, player_stats_data):
    filename = f"csv/basketball/matchStatistics/{game_id}_matchStatistics.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Local", "Stats", "Visitor","Game ID"])
        for row in player_stats_data:
            row.append(game_id)  # Add the Game ID to the row data
            writer.writerow(row)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
