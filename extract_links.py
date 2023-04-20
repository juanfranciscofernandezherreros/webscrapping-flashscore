import asyncio
from pyppeteer import launch

async def extract_links(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    links = await page.querySelectorAll('a')
    hrefs = []
    for link in links:
        href = await page.evaluate('(element) => element.href', link)
        if href:
            hrefs.append(href)
    await browser.close()
    return hrefs
