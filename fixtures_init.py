import asyncio
import csv
from pyppeteer import launch
from datetime import datetime
from urllib.parse import urlparse
import glob
import os

async def main():
    uri = "https://www.flashscore.com/basketball/spain/acb/fixtures/"
    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball") 
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "lineups"
    urls_folder = os.path.join(basketball_folder, "fixtures")
    if not os.path.exists(urls_folder):
        os.mkdir(urls_folder)

    # Launch the browser
    browser = await launch(headless=False)
    
    # Open a new page
    page = await browser.newPage()
    
    # Go to the desired URL
    await page.goto(uri)
   
    # Get all elements that contain the class name "event"
    
    elements = await page.querySelectorAll('[id^="g_3"]')
    ids = []
    for element in elements:
        property = await element.getProperty('id')
        value = await property.jsonValue()
        ids.append(value)
        
    events = await page.querySelectorAll('.event__time')
    eventHome = await page.querySelectorAll('.event__participant--home')
    awayHome = await page.querySelectorAll('.event__participant--away')
    # Create an empty list to store the data
    data = []
    
    uri_parts = uri.split("/")
    text = f"{uri_parts[4]} {uri_parts[5]} {uri_parts[6]}"
    result = "{}_{}_{}".format(*text.split())
    
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%d_%H_%M_%S")
    time_str = time_str.replace(":", "_")
            
    # Extract the text content of each element and append to the data list
    for i in range(len(events)):
        identificador = ids[i]
        event_text = await page.evaluate('(element) => element.textContent', events[i])
        home_text = await page.evaluate('(element) => element.textContent', eventHome[i])
        away_text = await page.evaluate('(element) => element.textContent', awayHome[i])

        split_string = event_text.split(". ")
        date_string = split_string[0]        
        time_string = split_string[1]

        # Get current year and format it as "yyy"
        current_year = datetime.now().strftime("%Y")[-4:]

        # Add the year to the time string
        # Add the year to the time string
        time_string_with_year = f"{date_string}.{current_year}-{time_string}"
        timeLong = time_string_with_year

        # Parse the date string and convert it to a datetime object
        date_time_obj = datetime.strptime(timeLong, "%d.%m.%Y-%H:%M")
        timestamp = int(date_time_obj.timestamp())
        
        data.append([timestamp, time_string_with_year, home_text, away_text, identificador])
    # extract the domain name from the URL
    parsed_url = urlparse(uri)
    domain_name = parsed_url.netloc.replace('.', '_')

    # use the domain name as the file name
    file_name = f'{domain_name}.csv'
    
    # Print the data
    # Open the CSV file in write mode
    with open('csv/basketball/fixtures/'+result+"_"+time_str+".csv", mode='w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file, delimiter=';')

        # Write the headers to the CSV file
        headers = ['EventTimeUTC','EventTimeUTC', 'homeTeam', 'awayTeam', 'matchId']
        writer.writerow(headers)

        # Write the rows to the CSV file
        for d in data:
            writer.writerow(d)

    # Close the CSV file
    csv_file.close()
    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
