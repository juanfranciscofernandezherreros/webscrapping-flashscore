import asyncio
from pyppeteer import launch

async def scrape_website():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.flashscore.es/')

    live_leagues = await page.querySelectorAll('.leagues--live')
    for league in live_leagues:
        league_children = await league.querySelectorAll('*')
        for child in league_children:
            if await child.getProperty('className') and 'event__participant--home' in await child.getProperty('className').jsonValue():
                home_team_name = await page.evaluate('(child) => child.textContent', child)
                score_data = await child.getProperty('nextElementSibling')
                score = await score_data.getProperty('textContent')
                score_text = await score.jsonValue()
                away_team_data = await score_data.getProperty('nextElementSibling')
                away_team = await away_team_data.querySelector('.event__participant--away')
                away_team_name = await page.evaluate('(away_team) => away_team.textContent', away_team)
                print(f"{home_team_name.strip()} {score_text.strip()} {away_team_name.strip()}")

    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape_website())