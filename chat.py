import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send GET request to FlashScore website and retrieve HTML content
url = "https://www.flashscore.com/football/"
response = requests.get(url)
content = response.content

# Parse HTML content and extract relevant data using BeautifulSoup
soup = BeautifulSoup(content, "html.parser")
print(soup)
# Create a list of dictionaries to store the scraped data
data = []
for match in matches:
    team1 = match.find("div", {"class": "event__participant--home"}).text.strip()
    team2 = match.find("div", {"class": "event__participant--away"}).text.strip()
    score1 = match.find("div", {"class": "event__scores fontBold"}).text.strip().split(":")[0]
    score2 = match.find("div", {"class": "event__scores fontBold"}).text.strip().split(":")[1]
    data.append({"Team 1": team1, "Team 2": team2, "Score 1": score1, "Score 2": score2})

# Create a DataFrame from the list of dictionaries using pandas
df = pd.DataFrame(data)

# Print or export the DataFrame as desired
print(df)
