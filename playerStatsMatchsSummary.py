import asyncio
import csv
import sys
from pyppeteer import launch
import exportarCsv
import os 
import datetime
#py playerStatsMatchsSummary.py https://www.flashscore.com/match/6eSbIzWE/#/match-summary/player-statistics/0
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
    #Match Id
    matchId = url.split('/')[4]
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
                data = []
                count = len(await page.querySelectorAll('#detail > div.section.psc__section > div > div.ui-table.playerStatsTable > div.ui-table__body > div:nth-child(n)'))
                for i in range(1, count+1):
                    selector = f'#detail > div.section.psc__section > div > div.ui-table.playerStatsTable > div.ui-table__body > div:nth-child({i}) > *'
                    selectorHrefs = f'#detail > div.section.psc__section > div > div.ui-table.playerStatsTable > div.ui-table__body > div:nth-child({i}) > a'
                    elementsLinks = await page.querySelectorAll(selectorHrefs) # get all anchor tags in the row
                    elements = await page.querySelectorAll(selector)
                    row = []
                    for element in elements:
                        element_text = await page.evaluate('(element) => element.textContent', element)
                        row.append(element_text)
                    for elementLink in elementsLinks:
                        href = await page.evaluate('(element) => element.href', elementLink) # get href attribute of the first anchor tag
                        playerId = href.split('/')[5]
                        row.append(playerId)
                        row.append(matchId)
                    data.append(row)
                header = "namePlayer, team, pts, reb, ast, mins, fgm, fga, two_pm,two_pa, three_pm, three_pa, ftm, fta, valoracion, offensiverebounds,deffensiverebounds, personalFours, steals, turnovers,blockedShot, blockedAgains, technicalFouls, playerId, matchId "
                filename = f"{id}_stats.csv"
                exportarCsv.exportarCsv(data, header, "csv/basketball/summary/"+filename)
            if "/match-summary/lineups" in href:                
                await page.goto(href)
                # Get all elements with the class name "lf__participantNumber"
                await asyncio.sleep(5)
                participantNumber = await page.querySelectorAll('.lf__participantNumber')

                # Extract the text content of each element
                number = []
                for element in participantNumber:
                    text = await page.evaluate('(element) => element.textContent', element)
                    number.append(text)    

                print(number)
                
                # Get all elements with the class name "lf__participantNumber"
                participantName = await page.querySelectorAll('.lf__participantName')
                
                # Get all links and extract the "href" attribute value for the player pages
                ids = []
                links = await page.querySelectorAll('a')
                for link in links:
                    href = await page.evaluate('(element) => element.href', link)        
                    if href and 'player' in href and href.count('/') == 6:
                        split_href = href.split("/")
                        result = split_href[-2]
                        ids.append(result)
                print(ids)

                # Extract the text content of each ".lf__participantName" element
                texts = []
                for element in participantName:
                    text = await page.evaluate('(element) => element.textContent.trim()', element)
                    texts.append(text)    

                print(texts)
                
                # Combine the arrays into a bidimensional array
                results = []
                for i in range(len(number)):
                    item = [number[i], texts[i], ids[i]]
                    if i < 10:
                        item.append('Starter')
                    else:
                        item.append('Substitute')
                    results.append(item)         
                
                url_parts = url.split("/")
                match_id = url_parts[4]
                print(match_id)
                
                # Write data to CSV file
                with open(f"csv/basketball/lineups/lineups_{match_id}.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['numberPlayer', 'namePlayer', 'playerId', 'Starter', 'MatchId'])
                    for row in results:
                        row.insert(4, match_id)
                        writer.writerow(row)
            if "/match-summary/point-by-point" in href: 
                print("PointByPoint")
                await page.goto(href)
                await asyncio.sleep(5)
                result_array = []
                count = await page.evaluate('''
                    () => {
                        // Seleccionar todos los elementos que coincidan con el selector CSS
                        const elements = document.querySelectorAll('.matchHistoryRow');
                        // Obtener la cantidad de elementos encontrados
                        return elements.length;
                    }
                ''')
                print(f'El elemento aparece {count} veces en la página.')
                
                for i in range(2, count+2):
                    
                    xpath = f'//*[@id="detail"]/div[9]/div[{i}]/div[1]'
                    xpath1 = f'//*[@id="detail"]/div[9]/div[{i}]/div[2]/div[1]'
                    xpath2 = f'//*[@id="detail"]/div[9]/div[{i}]/div[2]/div[2]'
                    xpath3 = f'//*[@id="detail"]/div[9]/div[{i}]/div[3]'

                    element = await page.xpath(xpath)
                    element1 = await page.xpath(xpath1)
                    element2 = await page.xpath(xpath2)
                    element3 = await page.xpath(xpath3)

                    text = await element[0].getProperty('textContent')
                    text1 = await element1[0].getProperty('textContent')
                    text2 = await element2[0].getProperty('textContent')
                    text3 = await element3[0].getProperty('textContent')

                    text = await text.jsonValue()
                    text1 = await text1.jsonValue()
                    text2 = await text2.jsonValue()
                    text3 = await text3.jsonValue()

                    row = []
                    if text.strip() != "":
                        row.append(text)
                    else:
                        row.append("-")
                    if text1.strip() != "":
                        row.append(text1)
                    else:
                        row.append("-")
                    if text2.strip() != "":
                        row.append(text2)
                    else:
                        row.append("-")
                    if text3.strip() != "":
                        row.append(text3)
                    else:
                        row.append("-")
                    
                    result_array.append(row)
                
                url_parts = url.split("/")
                match_id = url_parts[8]
                match_type = url_parts[6]
                match_number = url_parts[4]
                print(match_id)
                print(match_type)
                print(match_number)

                # Write data to CSV file
                with open(f"csv/basketball/pointByPoint/pointByPoint_{match_id}_{match_number}.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Name', 'Home', 'Away', 'Time', 'MatchId', 'MatchNumber'])
                    for row in result_array:
                        row.append(match_id)
                        row.insert(4, match_number)
                        writer.writerow(row)
                
    await browser.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py url")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))
