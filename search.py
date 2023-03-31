import argparse
import asyncio
import csv
import mysql.connector
from pyppeteer import launch
from datetime import datetime  # add this import
import os

async def main(url=None):
    
    # Connect to the MySQL server
    db = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )
    
    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "urls"
    urls_folder = os.path.join(basketball_folder, "urls")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

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
        inserted_hrefs = []
        errored_hrefs = []
        for href in filtered_hrefs:
            try:
                insert_query = "INSERT INTO urls (urls, isOpened) VALUES (%s, %s)"
                val = (href, 'F')
                mycursor.execute(insert_query, val)
                db.commit()
                inserted_count += 1
                inserted_hrefs.append({'href': href, 'sql_query': insert_query})
            except Exception as e:
                error_msg = f"Error inserting href {href}: {str(e)}"
                print(error_msg)
                errored_hrefs.append({'href': href, 'error_msg': error_msg})
                error_count += 1

        # Save inserted and errored hrefs to CSV files
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"csv/basketball/urls/inserted_hrefs_{now}.csv", mode='w') as file:
            fieldnames = ['href', 'sql_query']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for href in inserted_hrefs:
                writer.writerow(href)
                    
        with open(f"csv/basketball/urls/errored_hrefs_{now}.csv", mode='w') as file:
            fieldnames = ['href', 'error_msg']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for href in errored_hrefs:
                writer.writerow(href)
        
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