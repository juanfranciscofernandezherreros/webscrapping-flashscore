import argparse
import mysql.connector
import config.database
import time
from pyppeteer import launch

def count_unopened_urls():
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    query = ("SELECT COUNT(*) FROM urls WHERE isOpened = 'F'")
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    return count

def get_unopened_urls():
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    query = ("SELECT urls FROM urls WHERE isOpened = 'F'")
    cursor.execute(query)
    urls = cursor.fetchall()
    cursor.close()
    cnx.close()
    return urls

def insert_url(url):
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    add_url = ("INSERT INTO urls "
               "(urls, isOpened) "
               "VALUES (%s, 'F')")
    data_url = (url,)
    cursor.execute(add_url, data_url)
    cnx.commit()
    cursor.close()
    cnx.close()

def update_url(url):
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    update_url = ("UPDATE urls "
                  "SET isOpened = 'T' "
                  "WHERE urls = %s")
    data_url = (url,)
    cursor.execute(update_url, data_url)
    cnx.commit()
    cursor.close()
    cnx.close()

def check_url_exists(url):
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    query = ("SELECT urls FROM urls WHERE urls=%s")
    data_url = (url,)
    cursor.execute(query, data_url)
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result is not None

async def extract_hrefs(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    hrefs = await page.evaluate('''() => {
        return [...document.querySelectorAll('a')].map(elem => elem.href);
    }''')
    await browser.close()
    return hrefs


def main(url=None):
    if url:
        print(f"La URL proporcionada es {url}.")
        if(check_url_exists(url) == False):
            insert_url(url)
    else:
        print("No se proporcionó ninguna URL.")
        
    while True:
        count = count_unopened_urls()
        if count > 0:
            urls = get_unopened_urls()
            for url in urls:
                print(f"Abriendo URL: {url[0]}")
                
                update_url(url[0])
                # Code to open the URL goes here
                time.sleep(5) # wait for 5 seconds before opening the next URL
        else:
            print("No hay URLs por abrir.")
            break
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script que acepta una URL opcionalmente.')
    parser.add_argument('url', nargs='?', help='URL opcional.')
    args = parser.parse_args()
    main(args.url)
