import argparse
import asyncio
import csv
import mysql.connector
from pyppeteer import launch
import os
import datetime
# Connect to the MySQL server
import config.database

async def main(url):    

    # Connect to the MySQL server
    db = config.database.conectar()

    # Check if the connection was successful
    if db.is_connected():
        print("Connected to database")
    else:
        print("Failed to connect to database")
        return
    
    cursor = db.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id BIGINT NOT NULL AUTO_INCREMENT,
                urls VARCHAR(200) UNIQUE,
                country VARCHAR(200),
                isOpened VARCHAR(200),    
                whenHasOpened int,
                PRIMARY KEY (id)
            )
        """)       
    db.commit()
    cursor.close()   
     
    # Get list of emails to send
    # Create a cursor object
    mycursor = db.cursor()

    # Generate the SELECT statement
    select_query = "SELECT urls,isOpened FROM urls WHERE isOpened='F'"

    # Execute the SELECT query
    mycursor.execute(select_query)    
    
    # Get the results
    results = mycursor.fetchall()
    
    while True: 

         

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
                finally:
                    cursor.close()

                # Scrape the page
                browser = await launch(headless=True)
                page = await browser.newPage()
                print("URL")
                print(url)
                await page.goto(url)
                
                hrefs = []
                links = await page.querySelectorAll('a')
                for link in links:
                    href = await page.evaluate('(element) => element.href', link)
                    if href:
                        hrefs.append(href)
                await browser.close()
                
                # Update the database to mark the url as opened
                update_sql = "UPDATE urls SET isOpened = 'T' WHERE urls = '"+url+"'"
                cursor = db.cursor()
                try:
                    cursor.execute(update_sql)
                    db.commit()
                except mysql.connector.Error as error:
                    db.rollback()
                finally:
                    cursor.close()
                    
                
                # Get current date and time
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Construct file name with timestamp
                filename = f"urls_{timestamp}"
                                  
                # Filter and store the urls
                filtered_hrefs = set(filter(lambda x: 'basketball' in x and x.count('/') in [5, 6, 7], hrefs))
                sql = "INSERT INTO urls (urls, isOpened) VALUES (%s, 'F')"
                inserted_count = 0
                error_count = 0
                errorSql = []
                # Create an empty list to hold the rows that failed to insert
                error_rows = []
                for row in filtered_hrefs:
                    values = (row,)
                    cursor = db.cursor()
                    try:
                        cursor.execute(sql, values)
                        db.commit()
                        inserted_count += 1
                    except mysql.connector.errors.IntegrityError as error:
                        if "Duplicate entry" not in str(error):
                            error_rows.append({"error": str(error)})
                        db.rollback()
                    finally:
                        cursor.close()                                            
                 
                # Export the error rows to a CSV file
                if len(error_rows) > 0:
                    
                    # Define the name of the CSV file
                    csv_filename = f"csv/basketball/errors/url_errors_{timestamp}.csv"

                    # Write the error rows to the CSV file
                    with open(csv_filename, mode='w', newline='') as error_file:
                        error_writer = csv.writer(error_file)
                        error_writer.writerow(['Failed Row', 'Error Message'])
                        error_writer.writerows(error_rows)
                    
                    # Insert the database to mark the url as opened
                    insertSql = "INSERT INTO errors_events (nameScriptPython,nameCsvWithErrors,success,errors) VALUES (%s,%s,%s,%s)"
                    cursor = db.cursor()
                    filename = os.path.basename(__file__)
                    try:
                        cursor.execute(insertSql, (filename, csv_filename, inserted_count, error_count))
                        db.commit()
                    except mysql.connector.Error as error:
                        db.rollback()
                    finally:
                        cursor.close()
                    # Get the current date and time
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    

        else:
            sql = "INSERT INTO urls (urls, isOpened) VALUES (%s, 'F')"
            values = (url,)
            cursor = db.cursor()
            try:
                cursor.execute(sql, values)
                db.commit()
            except mysql.connector.Error as error:
                db.rollback()
            finally:
                cursor.close()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract all hrefs from a web page')
    parser.add_argument('url', type=str, help='URL of the web page')
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(main(args.url))