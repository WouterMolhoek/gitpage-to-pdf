import urllib.request
from bs4 import BeautifulSoup
from fpdf import FPDF
import webbrowser

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

    # Get all the repositories on the first page
    repositories = repos.find_all(itemprop='owns')

    return [profile_img, repositories, contribution, name, username]


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

    pdf.x = 110
    pdf.y = 8
    pdf.set_font('Arial', 'B', 22)
    pdf.multi_cell(80, 10, data[3], 0, 'L')
    pdf.x = 110
    pdf.y = 16
    pdf.set_font('Arial', '', 18)
    pdf.multi_cell(80, 10, data[4], 0, 'L')

    pdf.y = 120
    pdf.x = 22
    pdf.multi_cell(50, 10, 'Repositories', 0, 'L')
    pdf.x = 115
    pdf.y = 120
    pdf.multi_cell(50, 10, 'Contribution', 0, 'L')

    file_name = 'Github-Profile-(' + data[3] + ').pdf'

    # Save the file (add profile name)
    pdf.output(file_name)

    # Open the created file
    webbrowser.open_new(file_name)

create_pdf()