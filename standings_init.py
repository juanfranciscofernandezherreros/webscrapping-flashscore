import asyncio
import csv
from pyppeteer import launch
from datetime import datetime
from urllib.parse import urlparse
import glob
import os
import mysql.connector
import asyncio
import resultsMatch
import config.database
import sys
import os
import fixtures_init

async def extract_table_data():
    # Launch a headless Chrome browser
    browser = await launch()
    page = await browser.newPage()

    # Navigate to the webpage containing the table
    await page.goto('https://www.flashscore.com/basketball/spain/acb/standings/')

    # Wait for the table to load
    await page.waitForSelector('.ui-table__row')

    # Extract the table data
    table_data = []
    rows = await page.querySelectorAll('.ui-table__row')
    for row in rows:
        cells = await row.querySelectorAll('.table__cell--participant, .table__cell--value')
        row_data = []
        for cell in cells:
            cell_text = await page.evaluate('(element) => element.textContent', cell)
            row_data.append(cell_text.strip())
        table_data.append(row_data)

    # Close the browser
    await browser.close()

    return table_data

# Run the extraction function asynchronously
table_data = asyncio.get_event_loop().run_until_complete(extract_table_data())

# Print the extracted data
for row in table_data:
    print(row)

if __name__ == '__main__':
    asyncio.run(extract_table_data())
