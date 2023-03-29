import argparse
import asyncio
import csv
import mysql.connector
from pyppeteer import launch
#py searchFinal.py https://www.flashscore.com/basketball/spain/
async def main(url):

    # Connect to the MySQL server
    db = mysql.connector.connect(
        host="localhost",
        user="user_bigdataetl",
        password="password_bigdataetl",
        database="bigdataetl"
    )
    
    #Get list of emails to send
    # Create a cursor object
    mycursor = db.cursor()

    # Generate the SELECT statement
    select_query = "SELECT urls,isOpened FROM urls WHERE isOpened='F'"

    # Execute the SELECT query
    mycursor.execute(select_query)
    
    # Get the results
    results = mycursor.fetchall()
    
     # Check if the result is not empty

    # Check if the result is not empty
    if len(results) > 0:
        # Iterate over the results
        print("Len: " + str(len(results)))
        for row in results:
                email = row[0]
                # Do something with the email                
    
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
       
    print("URL" + url)    

    # Prepare SQL statement
    update_sql = "UPDATE urls SET isOpened = 'T' WHERE urls = '"+url+"'"
    
    print("Update SQL" + update_sql)
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
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract all hrefs from a web page')
    parser.add_argument('url', type=str, help='URL of the web page')
    args = parser.parse_args()
    asyncio.get_event_loop().run_until_complete(main(args.url))