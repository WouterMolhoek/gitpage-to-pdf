import urllib.request
from bs4 import BeautifulSoup
from fpdf import FPDF


# Repositories URL
url_repos = 'https://github.com/WouterMolhoek?tab=repositories'
# Github Profile URL
url_profile = 'https://github.com/WouterMolhoek'


# Scrape data from the given URL
def scrape_raw_data(url):
    # Query the website (url) and return the html
    page = urllib.request.urlopen(url)

    # Parse the html using beautiful soup and store in variable `soup`
    return BeautifulSoup(page, 'html.parser')


def format_req_data():
    profile = scrape_raw_data(url_profile)
    repos = scrape_raw_data(url_repos)

    # Get the profile image
    profile_img = profile.find(class_='avatar width-full avatar-before-user-status')['src']

    # Get the profile name
    name = profile.find(itemprop='name').get_text()

    # Get the contribution activity
    contribution = profile.find(class_='f4 text-normal mb-2').get_text()

    # Get the programmingLanguage item property
    programming_lan = repos.find_all(itemprop='programmingLanguage')

    # Remove duplicate languages
    programming_lan = list(dict.fromkeys(programming_lan))
    languages = []

    # Get innerText from the items and store that in the languages list
    for language in programming_lan:
        languages.append(language.get_text())

    return [profile_img, languages, contribution, name]


def download_image(url):
    name = 'profile-image'
    fullname = str(name)+".jpg"
    urllib.request.urlretrieve(url, fullname)


def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    data = format_req_data()

    # Download profile image
    download_image(data[0])

    # Add layout-image to the page
    pdf.image('layout-pdf.jpg', x=0, y=0, w=210)
    pdf.cell(200, 10, txt="{}".format(''), ln=1)

    # Add profile-image to the page
    pdf.image('profile-image.jpg', x=10, y=10, w=70)
    pdf.cell(200, 10, txt="{}".format(''), ln=1)

    # Add UserName
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 0, txt=data[3], ln=1, align="C")

    pdf.output("Github-Profile.pdf")


create_pdf()