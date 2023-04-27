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
        if tab_text == "Summary":
            print("Summary")
            summary_data = await _get_summary_data(page)
            await _write_summary_to_csv(game_id, summary_data)    

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


async def _write_summary_to_csv(game_id, summary_data):
    filename = f"csv/basketball/summary/{game_id}_summary.csv"
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Game ID", "Total Home", "Total Away", "Q1 Local", "Q1 Away", "Q2 Local", "Q2 Away", "Q3 Local", "Q3 Away", "Q4 Local", "Q4 Away", "Q5 Local", "Q5 Away"])
        writer.writerow([game_id, summary_data["total_home"], summary_data["total_away"]] + summary_data["quarter_scores"])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
