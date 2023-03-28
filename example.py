import asyncio
from pyppeteer import launch

async def scrape_website():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.flashscore.es/')

    elements = await page.querySelectorAll('[id^="g_3"]')
    element_texts = []
    for element in elements:
        element_text = await page.evaluate('(element) => element.textContent', element)
        element_texts.append(element_text)

    print(element_texts)

    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape_website())
