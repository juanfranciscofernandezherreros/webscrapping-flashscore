from pyppeteer import launch
import asyncio

async def scrape_links(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    hrefs = await page.evaluate('''() => {
        return [...document.querySelectorAll('a')].map(elem => elem.href);
    }''')
    await browser.close()
    return hrefs
