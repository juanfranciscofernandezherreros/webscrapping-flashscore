#python index2.py https://www.flashscore.com/basketball/ 
import argparse
import asyncio
import config.database
import time
from pyppeteer import launch

def create_urls_table():
    """Comprobar si existe la tabla urls"""    
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    query = ("CREATE TABLE IF NOT EXISTS urls ("
             "id BIGINT NOT NULL AUTO_INCREMENT,"
             "urls VARCHAR(200) UNIQUE,"
             "country VARCHAR(200),"
             "isOpened VARCHAR(200),"
             "whenHasOpened int,"
             "PRIMARY KEY (id)"
             ")")
    cursor.execute(query)
    cnx.commit()
    cursor.close()
    cnx.close()


def count_unopened_urls():
    """Cuenta la cantidad de URLs que aún no han sido abiertas"""    
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    query = ("SELECT COUNT(*) FROM urls WHERE isOpened = 'F'")
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    cnx.close()
    return count

def get_unopened_urls():
    """Obtiene una lista de URLs que aún no han sido abiertas"""
    cnx = config.database.conectar()
    cursor = cnx.cursor()
    query = ("SELECT urls FROM urls WHERE isOpened = 'F'")
    cursor.execute(query)
    urls = cursor.fetchall()
    cursor.close()
    cnx.close()
    return urls

def insert_url(url):
    """Inserta una nueva URL en la base de datos"""
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
    """Actualiza el estado de una URL a 'abierta' en la base de datos"""
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
    """Verifica si una URL ya existe en la base de datos"""
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
    """Extrae los enlaces (hrefs) de una página web"""
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    hrefs = await page.evaluate('''() => {
        return [...document.querySelectorAll('a')].map(elem => elem.href);
    }''')
    await page.close()
    await browser.close()
    filtered_hrefs = set(filter(lambda x: 'basketball' in x and x.count('/') in [5, 6, 7] and 'news' not in x, hrefs))
    return filtered_hrefs

async def main(url=None):
    """Función principal que ejecuta el script"""
    if url:
        print(f"La URL proporcionada es {url}.")
        if(check_url_exists(url) == False):
            insert_url(url)
    else:
        print("No se proporcionó ninguna URL.")

    start_time = time.time()
    time_limit_reached = False  # added flag to keep track of time limit

    while not time_limit_reached:       

        count = count_unopened_urls()
        if count > 0:
            urls = get_unopened_urls()
            for url in urls:

                iteration_time  = time.time()
                print("Start Time" , start_time)
                print("Iteration Time" , iteration_time)

                if time.time() - start_time >= 60:
                    print("Se ha alcanzado el tiempo límite de un minuto.")
                    time_limit_reached = True  # set flag to True
                    break  # break out of both loops
                else:
                    print(f"Abriendo URL: {url[0]}")                
                    # Scrape the page
                    hrefs = await extract_hrefs(url[0])
                    
                    # Do something with the extracted links
                    for href in hrefs:
                        print(f"Extracted link: {href}")
                        if(check_url_exists(href) == False):
                            insert_url(href)
                        else:
                            print("Ya existe este HREF",href)                                  
                    update_url(url[0])
                
        else:
            print("No hay URLs por abrir.")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script que acepta una URL opcionalmente.')
    create_urls_table()
    parser.add_argument('url', nargs='?', help='URL opcional.')
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.url))