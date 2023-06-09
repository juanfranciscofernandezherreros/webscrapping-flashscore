import asyncio
import csv
from pyppeteer import launch
from datetime import datetime
from urllib.parse import urlparse
import glob
import os

async def main(uri):

    # Make sure the "csv" folder exists
    if not os.path.exists("csv"):
        os.mkdir("csv")

    # Create a subfolder called "basketball"
    basketball_folder = os.path.join("csv", "basketball")
    if not os.path.exists(basketball_folder):
        os.mkdir(basketball_folder)

    # Create a subfolder called "lineups"
    urls_folder = os.path.join(basketball_folder, "results")
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
        p1_text = await page.evaluate('(element) => element.textContent', part1[i])
        p2_text = await page.evaluate('(element) => element.textContent', part2[i])
        p3_text = await page.evaluate('(element) => element.textContent', part3[i])
        p4_text = await page.evaluate('(element) => element.textContent', part4[i])
        
        p1_away = await page.evaluate('(element) => element.textContent', part1_away[i])
        p2_away = await page.evaluate('(element) => element.textContent', part2_away[i])
        p3_away = await page.evaluate('(element) => element.textContent', part3_away[i])
        p4_away = await page.evaluate('(element) => element.textContent', part4_away[i])                             
        
        split_string = event_text.split(". ")
        date_string = split_string[0]        
        time_string = split_string[1]

        # Get current year and format it as "yyy"
        current_year = datetime.now().strftime("%Y")[-4:]

        # Add the year to the time string
        time_string_with_year = f"{date_string}.{current_year}-{time_string}"

        # Check if event_text contains "AOT"
        if "AOT" in event_text:
            event_code = event_text[:-3]      
            split_string = event_code.split(". ")
            date_string = split_string[0]        
            time_string = split_string[1]

            # Get current year and format it as "yyy"
            current_year = datetime.now().strftime("%Y")[-4:]

            # Add the year to the time string
            time_string_with_year = f"{date_string}.{current_year}-{time_string}"
            timeLong = time_string_with_year
            
            part5 = await page.querySelector(f'div[id^="g_3"] .event__part.event__part--away.event__part--5')
            part5_home = await page.querySelector(f'div[id^="g_3"] .event__part.event__part--home.event__part--5')
            if part5:
                p5_text_away = await page.evaluate('(element) => element.textContent', part5)
                p5_text_home = await page.evaluate('(element) => element.textContent', part5_home)
            else:
                p5_text_away = ""
                p5_text_home = ""
        else:
            timeLong = time_string_with_year
            p5_text_away = ""
            p5_text_home = ""
        
        
        # Parse the date string and convert it to a datetime object
        date_time_obj = datetime.strptime(timeLong, "%d.%m.%Y-%H:%M")
        timestamp = int(date_time_obj.timestamp())
        
        data.append([timestamp, time_string_with_year, home_text, away_text, p1_text, p2_text, p3_text, p4_text, p5_text_home,p1_away,p2_away,p3_away,p4_away,p5_text_away,identificador,uri_parts[4],uri_parts[5]])
    # extract the domain name from the URL
    parsed_url = urlparse(uri)
    domain_name = parsed_url.netloc.replace('.', '_')

    # use the domain name as the file name
    file_name = f'{domain_name}.csv'
    
    # Print the data
    # Open the CSV file in write mode
    with open('csv/basketball/results/'+result+"_"+time_str+".csv", mode='w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file, delimiter=';')

        # Write the headers to the CSV file
        headers = ['Event Time UTC','Event Time', 'Home Team', 'Away Team', '1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter', 'Overtime Home', '1st Quarter Away', '2nd Quarter Away', '3rd Quarter Away', '4th Quarter Away', 'Overtime Away','MatchId','Country','Competition']
        writer.writerow(headers)

        # Write the rows to the CSV file
        for d in data:
            writer.writerow(d)

    # Close the CSV file
    csv_file.close()
    await browser.close()
