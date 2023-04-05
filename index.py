# -*- coding: latin-1 -*-
#INSERT INTO bigdataetl.urls (urls, country, isOpened, whenHasOpened) VALUES('https://www.flashscore.com/basketball/', '-', 'F', 0);
# UPDATE urls SET isOpened = 'T'
#DELETE FROM urls
import requests
import time
import mysql.connector
import asyncio
import argparse
import datetime
from pyppeteer import launch


def consulta_count(mycursor):
    # Generate the SELECT statement
    select_query = "SELECT urls,isOpened FROM urls WHERE isOpened='F'"
    # Execute the SELECT query
    mycursor.execute(select_query)        
    # Get the results
    results = mycursor.fetchall()
    return results

async def scrape_url(url):
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
    return hrefs

async def main():
        # Conecta a la base de datos
        mydb = mysql.connector.connect(
            host="localhost",
            user="user_bigdataetl",
            password="password_bigdataetl",
            database="bigdataetl"
        )
        
        if mydb.is_connected():
            print("Connected to database")
               
        
        mycursor = mydb.cursor()
        
        mycursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    urls VARCHAR(200) UNIQUE,
                    country VARCHAR(200),
                    isOpened VARCHAR(200),    
                    whenHasOpened int,
                    PRIMARY KEY (id)
                )
            """)       
        count = consulta_count(mycursor)
        print("Init Count")
        print(len(count))
        # Realiza la consulta count en la URL
        if len(count) > 0:                        
            opened_urls_count = 0
            for row in count:
                url = row[0]
                # Do something with the url

                # Update the database to mark the url as opened
                update_sql = "UPDATE urls SET isOpened = 'T' WHERE urls = '"+url+"'"
                cursor = mydb.cursor()
                try:
                    cursor.execute(update_sql)
                    mydb.commit()
                except mysql.connector.Error as error:
                    mydb.rollback()
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
                cursor = mydb.cursor()
                try:
                    cursor.execute(update_sql)
                    mydb.commit()
                except mysql.connector.Error as error:
                    mydb.rollback()
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
                    cursor = mydb.cursor()
                    try:
                        cursor.execute(sql, values)
                        mydb.commit()
                        inserted_count += 1
                    except mysql.connector.errors.IntegrityError as error:
                        if "Duplicate entry" not in str(error):
                            error_rows.append({"error": str(error)})
                        mydb.rollback()
                    finally:
                        cursor.close()
                count = consulta_count(mycursor)
                print(" Count")
                print(len(count))
                if len(count) == 0:                        
                    break

        time.sleep(1)

        
        # Cierra la conexin a la base de datos
        mydb.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
