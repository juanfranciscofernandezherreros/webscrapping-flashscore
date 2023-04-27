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

    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "lineups"
    urls_folder = os.path.join(basketball_folder, "summary")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)

    print("SUMMARY", url)
    
    # Obtener el id del partido
    name_file = url.split("/")[-4]+"_summary"
    game_id = url.split("/")[-4]

    # Seleccionar el elemento usando page.querySelector()
    total_home = await page.querySelector('.smh__part.smh__score.smh__home.smh__part--current')
    total_away = await page.querySelector('.smh__part.smh__score.smh__away.smh__part--current')

    # Obtener el texto del elemento usando page.evaluate()
    total__home = await page.evaluate('(element) => element.textContent', total_home)
    # Obtener el texto del elemento usando page.evaluate()
    total__away = await page.evaluate('(element) => element.textContent', total_away)

    quarters = ['1', '2', '3', '4', '5']

    with open(f"csv/basketball/summary/{name_file}.csv", "w", newline='') as f:
        writer = csv.writer(f)

        # Escribir la primera fila con los encabezados
        writer.writerow(["Game ID", "Total Home", "Total Away", "Q1 Local", "Q1 Away", "Q2 Local", "Q2 Away", "Q3 Local", "Q3 Away", "Q4 Local", "Q4 Away", "Q5 Local", "Q5 Away"])

        # Escribir la fila con los datos del partido
        row = [game_id, total__home, total__away]
        for q in quarters:
            quarter_local = await page.querySelector(f'.smh__part.smh__home.smh__part--{q}')
            quarter_away = await page.querySelector(f'.smh__part.smh__away.smh__part--{q}')
            quarter_local_text = await page.evaluate('(element) => element.textContent', quarter_local)
            quarter_away_text = await page.evaluate('(element) => element.textContent', quarter_away)
            row.append(quarter_local_text)
            row.append(quarter_away_text)

        writer.writerow(row)

    await browser.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
