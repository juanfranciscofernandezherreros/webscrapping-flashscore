import asyncio
from pyppeteer import launch

async def scrape_website():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.flashscore.com/basketball/')
    
    data = await page.evaluate('''() => {
        const games = Array.from(document.querySelectorAll('.event__match.event__match--static.event__match--oneLine'));

        return games.map(game => {
            const homeTeam = game.querySelector('.event__participant.event__participant--home').innerText.trim();
            const awayTeam = game.querySelector('.event__participant.event__participant--away').innerText.trim();
            const eventTime = game.querySelector('.event__time').innerText.trim() || '';

            return { homeTeam, awayTeam, eventTime };
        });
    }''')

    for game in data:
        if game['eventTime']:
            print(f"{game['homeTeam']} vs {game['awayTeam']}: {game['eventTime']}")
        else:
            print(f"{game['homeTeam']} vs {game['awayTeam']}")
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape_website())
