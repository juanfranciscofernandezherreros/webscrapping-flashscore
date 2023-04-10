import asyncio
import csv
import sys
from pyppeteer import launch
import exportarCsv
import os
import lineups

async def main(url):
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)
    # Obtener el elemento contenedor de los enlaces
    tabs_container = await page.waitForSelector('.tabs__group')
    # Obtener todos los elementos "a" dentro del contenedor
    tabs_links = await tabs_container.querySelectorAll('a')
    # Crear una lista para almacenar los enlaces
    hrefs = []
    # Iterar sobre los enlaces y obtener el valor del atributo "href"
    for link in tabs_links:
        href = await (await link.getProperty('href')).jsonValue()
        hrefs.append(href)

    # Obtener el elemento contenedor de los enlaces
    tabs_container = await page.waitForSelector('#detail > div.tabs.tabs__detail--nav > div')
    tabs_links = await tabs_container.querySelectorAll('a:nth-child(n)')
    count = len(tabs_links)
    # Iterar sobre los enlaces y obtener el valor del atributo "href"
    for i in range(1, count+1):
        # Obtener todos los elementos "a" dentro del contenedor con nth-child=i
        tabs_links = await tabs_container.querySelectorAll(f'a:nth-child({i})')
        # Iterar sobre los enlaces y obtener el valor del atributo "href"
        for link in tabs_links:
            href = await (await link.getProperty('href')).jsonValue()
            print("URL",href)
            id = href.split('/')[4]
            if "/match-summary/match-summary" in href:
                player_links = []
                player_info = []
                links = await page.querySelectorAll('div.ui-table__body a')
                for link in links:
                    href = await page.evaluate('(element) => element.href', link)
                    if href and "player" in href and href not in player_links:
                        player_id = href.split('/')[-2]
                        player_name = href.split('/')[-3]       
                        # Agregar el nombre y el id del jugador a la lista
                        player_info.append([player_name, player_id])              
                #Exportar CSV                    
                header = "namePlayer,ids"
                filename = f"{id}_player.csv"
                exportarCsv.exportarCsv(player_info, header, "csv/basketball/players/"+filename)
            if "/match-summary/player-statistics" in href:
                print("OK")
    await browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
