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

# Remove duplicates
programming_lan = list(dict.fromkeys(programming_lan))

# Get the profile image
profile_img = soup.find(class_='avatar width-full avatar-before-user-status')

for language in programming_lan:
    print(language.get_text())

