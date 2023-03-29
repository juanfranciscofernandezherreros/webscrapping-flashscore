import argparse
import asyncio
import csv
import mysql.connector
from pyppeteer import launch

async def main(url):
    # Connect to the MySQL server
    db = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )

    while True:
        # Get list of emails to send
        # Create a cursor object
        mycursor = db.cursor()

        # Generate the SELECT statement
        select_query = "SELECT urls,isOpened FROM urls WHERE isOpened='F'"

        # Execute the SELECT query
        mycursor.execute(select_query)

        # Get the results
        results = mycursor.fetchall()

        # Check if the result is not empty
        if len(results) > 0:
            # Iterate over the results
            print("Len: " + str(len(results)))
            for row in results:
                url = row[0]
                # Do something with the url

                # Update the database to mark the url as opened
                update_sql = "UPDATE urls SET isOpened = 'T' WHERE urls = '"+url+"'"
                cursor = db.cursor()
                try:
                    cursor.execute(update_sql)
                    db.commit()
                except mysql.connector.Error as error:
                    db.rollback()
                    print("Error updating row: {}".format(error))
                finally:
                    cursor.close()

                # Scrape the page
                browser = await launch(headless=True)
                page = await browser.newPage()
                await page.goto(url)
                hrefs = []
                links = await page.querySelectorAll('a')
                for link in links:
                    href = await page.evaluate('(element) => element.href', link)
                    if href:
                        hrefs.append(href)
                await browser.close()

                # Filter and store the urls
                filtered_hrefs = set(filter(lambda x: 'basketball' in x and x.count('/') in [5, 6, 7], hrefs))
                sql = "INSERT INTO urls (urls, isOpened) VALUES (%s, 'F')"
                for row in filtered_hrefs:
                    values = (row,)
                    cursor = db.cursor()
                    try:
                        print(sql)
                        cursor.execute(sql, values)
                        db.commit()
                    except mysql.connector.Error as error:
                        db.rollback()
                        print("Error inserting row {}: {}".format(row, error))
                    finally:
                        cursor.close()
        else:
            # If no results were found, exit the loop
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract all hrefs from a web page')
    parser.add_argument('url', type=str, help='URL of the web page')
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(main(args.url))
