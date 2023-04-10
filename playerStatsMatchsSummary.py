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
        print(href)

    # Obtener el elemento contenedor de los enlaces
    tabs_container = await page.waitForSelector('#detail > div.tabs.tabs__detail--nav > div')
    tabs_links = await tabs_container.querySelectorAll('a:nth-child(n)')
    count = len(tabs_links)
    print(count)
    # Iterar sobre los enlaces y obtener el valor del atributo "href"
    for i in range(1, count+1):
        # Obtener todos los elementos "a" dentro del contenedor con nth-child=i
        tabs_links = await tabs_container.querySelectorAll(f'a:nth-child({i})')
        # Iterar sobre los enlaces y obtener el valor del atributo "href"
        for link in tabs_links:
            href = await (await link.getProperty('href')).jsonValue()
            hrefs.append(href)
            print(href)

    await browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
