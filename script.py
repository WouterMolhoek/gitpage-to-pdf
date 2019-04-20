import urllib.request
from bs4 import BeautifulSoup
from fpdf import FPDF

github = 'WouterMolhoek'

# Repositories URL
url_repos = 'https://github.com/' + github + '?tab=repositories'
# Github Profile URL
url_profile = 'https://github.com/' + github


# Scrape data from the given URL
def scrape_raw_data(url):
    # Query the website (url) and return the html
    page = urllib.request.urlopen(url)

    # Parse the html
    return BeautifulSoup(page, 'html.parser')


def format_req_data():
    profile = scrape_raw_data(url_profile)
    repos = scrape_raw_data(url_repos)

    # Get the profile image
    profile_img = profile.find(class_='u-photo d-block position-relative')['href']

    # Get the profile name
    name = profile.find(itemprop='name').get_text()

    # Get the username
    username = profile.find(itemprop='additionalName').get_text()

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

    return [profile_img, languages, contribution, name, username]


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

    # Add profile-image to the page
    pdf.image('profile-image.jpg', x=18, y=8, w=81, link=data[0])
    pdf.cell(200, 10, txt="{}".format(''), ln=1)

    # Add profile name, make it BOLD
    pdf.set_font("Arial", size=22, style="B")
    pdf.cell(264, -15, txt=data[3], ln=1, align="C")

    # Add username
    pdf.set_font("Arial", size=18)
    pdf.cell(249, 32, txt=data[4], ln=1, align="C")

    # Add repository heading
    pdf.set_font("Arial", size=22)
    pdf.cell(70, 180, txt='Repositories', ln=0, align="C")

    # Add Contribution heading
    pdf.set_font("Arial", size=22)
    pdf.cell(120, 180, txt='Contribution', ln=0, align="C")

    # Save the file (add profile name)
    pdf.output('Github-Profile-(' + data[3] + ').pdf')


create_pdf()