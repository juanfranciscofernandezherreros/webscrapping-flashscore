import asyncio
from pyppeteer import launch

async def main():
    # Launch the browser
    browser = await launch(headless=False)

    # Open a new page
    page = await browser.newPage()

    # Go to the desired URL
    await page.goto('https://www.flashscore.com/basketball')

    # Get all elements that contain the class name "event"
    events = await page.querySelectorAll('.event__stage--block')
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
        event_text = await events[i].textContent()
        home_text = await eventHome[i].textContent()
        away_text = await awayHome[i].textContent()
        p1_text = await part1[i].textContent()
        p2_text = await part2[i].textContent()
        p3_text = await part3[i].textContent()
        p4_text = await part4[i].textContent()
        p1_text_away = await part1_away[i].textContent()
        p2_text_away = await part2_away[i].textContent()
        p3_text_away = await part3_away[i].textContent()
        p4_text_away = await part4_away[i].textContent()
        data.append([event_text, home_text, away_text, p1_text, p2_text, p3_text, p4_text,p1_text_away,p2_text_away,p3_text_away,p4_text_away])

    # Print the data
    for d in data:
        print(d)

    # Close the browser
    await browser.close()

# Run the async function
asyncio.get_event_loop().run_until_complete(main())
