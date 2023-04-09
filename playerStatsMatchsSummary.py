import asyncio
import csv
import sys
from pyppeteer import launch
import exportarCsv

async def main(url):
    
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)

    # Obtener todos los elementos 'a' dentro de la clase 'tabs__group'
    links = await page.querySelectorAll('.tabs__group a')

    # Obtener la segunda parte del ID del partido de la URL
    id = url.split('/')[-5]

    # Hacer clic en cada enlace y tomar una captura de pantalla
    for i, link in enumerate(links):
        href = await page.evaluate('(element) => element.href', link)
        print(href)
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
    print(id)
    filename = f"{id}.csv"
    exportarCsv.exportarCsv(player_info, header, filename)
                            
    await browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
