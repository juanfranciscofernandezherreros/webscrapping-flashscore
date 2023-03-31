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
    
    #Get list of urls to open
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

            browser = await launch(headless=True)
            page = await browser.newPage()
            await page.goto(url)

            print("URL: " + url)

            # Prepare SQL statement
            update_sql = "UPDATE urls SET isOpened = 'T' WHERE urls = '"+url+"'"
            
            print("Update SQL: " + update_sql)

            # Execute the update statement
            cursor = db.cursor()

            try:
                cursor.execute(update_sql)
                db.commit()
            except mysql.connector.Error as error:
                db.rollback()
                print("Error updating row: {}".format(error))
            finally:
                cursor.close()

            hrefs = []
            links = await page.querySelectorAll('a')
            for link in links:
                href = await page.evaluate('(element) => element.href', link)
                if href:
                    hrefs.append(href)

            await browser.close()

            filtered_hrefs = set(filter(lambda x: 'basketball' in x and x.count('/') in [5, 6, 7], hrefs))

            # Prepare SQL statement
            sql = "INSERT INTO urls (urls, isOpened) VALUES (%s, 'F')"
            
            errors = []

            for row in filtered_hrefs:
                values = (row,)
                cursor = db.cursor()
                
                try:
                    cursor.execute(sql, values)
                    db.commit()            
                except mysql.connector.Error as error:
                    db.rollback()
                    error_msg = "Error inserting row {}: {}".format(row, error)
                    errors.append(error_msg)
                finally:
                    cursor.close()

            # Count the number of errors and print them
            num_errors = sum(1 for error in errors if error)
            print("Number of errors: {}".format(num_errors))   
            
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
