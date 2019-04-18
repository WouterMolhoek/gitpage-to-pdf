import urllib.request
from bs4 import BeautifulSoup

# Requested URL
url = 'https://github.com/WouterMolhoek/'

# Query the website (url) and return the html
page = urllib.request.urlopen(url)

# Parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

print(soup)
