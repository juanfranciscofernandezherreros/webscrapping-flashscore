import asyncio
from pyppeteer import launch

async def main():
    # Launch the browser
    browser = await launch(headless=False)

    # Open a new page
    page = await browser.newPage()

    # Go to the desired URL
    await page.goto('https://www.flashscore.com/basketball/usa/nba/results/')

    # Get all elements that contain the class name "event"
    events = await page.querySelectorAll('.event__time')
    eventHome = await page.querySelectorAll('.event__participant--home')
    awayHome = await page.querySelectorAll('.event__participant--away')
    part1 = await page.querySelectorAll('.event__part.event__part--home.event__part--1')
    part2 = await page.querySelectorAll('.event__part.event__part--home.event__part--2')
    part3 = await page.querySelectorAll('.event__part.event__part--home.event__part--3')
    part4 = await page.querySelectorAll('.event__part.event__part--home.event__part--4')
    
    part1_away = await page.querySelectorAll('.event__part.event__part--away.event__part--1')
    part2_away = await page.querySelectorAll('.event__part.event__part--away.event__part--2')
    part3_away = await page.querySelectorAll('.event__part.event__part--away.event__part--3')
    part4_away = await page.querySelectorAll('.event__part.event__part--away.event__part--4')
    
    # Create an empty list to store the data
    data = []

    # Extract the text content of each element and append to the data list
    for i in range(len(events)):              
        event_text = await page.evaluate('(element) => element.textContent', events[i])
        home_text = await page.evaluate('(element) => element.textContent', eventHome[i])
        away_text = await page.evaluate('(element) => element.textContent', awayHome[i])
        p1_text = await page.evaluate('(element) => element.textContent', part1[i])
        p2_text = await page.evaluate('(element) => element.textContent', part2[i])
        p3_text = await page.evaluate('(element) => element.textContent', part3[i])
        p4_text = await page.evaluate('(element) => element.textContent', part4[i])
        p1_text_away = await page.evaluate('(element) => element.textContent', part1_away[i])
        p2_text_away = await page.evaluate('(element) => element.textContent', part2_away[i])
        p3_text_away = await page.evaluate('(element) => element.textContent', part3_away[i])
        p4_text_away = await page.evaluate('(element) => element.textContent', part4_away[i])
        data.append([event_text, home_text, away_text, p1_text, p2_text, p3_text, p4_text,p1_text_away,p2_text_away,p3_text_away,p4_text_away])
        if "AOT" in event_text:
           part5_away = await page.querySelector('.event__part.event__part--away.event__part--5')
           p5_text_away = await page.evaluate('(element) => element.textContent', part5_away)
        else:
           p5_text_away = ""

    # Print the data
    for d in data:
        print(d)

    # Close the browser
    await browser.close()

# Run the async function
asyncio.get_event_loop().run_until_complete(main())