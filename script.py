import urllib.request
from bs4 import BeautifulSoup

# Requested URL
url = 'https://github.com/WouterMolhoek?tab=repositories'

# Query the website (url) and return the html
page = urllib.request.urlopen(url)

# Parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Get the programmingLanguage item property
programming_lan = soup.find_all(itemprop='programmingLanguage')

for language in programming_lan:
    print(language.get_text())

