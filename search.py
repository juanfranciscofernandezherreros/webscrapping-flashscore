import argparse
import asyncio
import csv
import mysql.connector
from pyppeteer import launch


async def main():

    # Connect to the MySQL server
    db = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )

    while True:
        # Get list of urls to open
        # Create a cursor object
        mycursor = db.cursor()

        # Generate the SELECT statement
        select_query = "SELECT urls FROM urls WHERE isOpened = 'F' LIMIT 1"
        # Execute the SELECT query
        mycursor.execute(select_query)

        # Get the result
        result = mycursor.fetchone()
        if result is None:
            print("No more urls to open. Sleeping for 10 seconds...")
            break

        url_to_open = result[0]

        # Take screenshot to get all hrefs that contain the word basketball and slash "5" "6" or "7"
        browser = await launch()
        page = await browser.newPage()
        print(f"url_to_open: {url_to_open}")
        await page.goto(url_to_open)
        await page.screenshot({'path': 'homepage.png'})
        hrefs = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a')).map(a => a.href);
        }''')
        await browser.close()

        filtered_hrefs = set(filter(lambda x: 'basketball' in x and x.count('/') in [5, 6, 7], hrefs))

        # Insert filtered hrefs into the database
        inserted_count = 0
        error_count = 0
        for href in filtered_hrefs:
            try:
                insert_query = "INSERT INTO urls (urls, isOpened) VALUES (%s, %s)"
                val = (href, 'F')
                mycursor.execute(insert_query, val)
                db.commit()
                inserted_count += 1
            except Exception as e:
                error_count += 1

        # Update URL state in database to 'T'
        update_query = "UPDATE urls SET isOpened = 'T' WHERE urls = %s"
        val = (url_to_open,)
        mycursor.execute(update_query, val)
        db.commit()

        # Print statistics
        print(f"Total urls to insert: {len(filtered_hrefs)}")
        print(f"Successfully inserted hrefs: {inserted_count}")
        print(f"Errored hrefs: {error_count}")
        
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
