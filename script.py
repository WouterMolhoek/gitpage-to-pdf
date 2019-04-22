import urllib.request
from bs4 import BeautifulSoup
from fpdf import FPDF
import webbrowser

github_account = 'WouterMolhoek'
github_url = 'https://github.com/'

# Repositories URL
url_repos = github_url + github_account + '?tab=repositories'
# Github Profile URL
url_profile = github_url + github_account
# Github Followers URL
url_followers = github_url + github_account + '?tab=followers'
# Github following URL
url_following = github_url + github_account + '?tab=following'

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

    # Get the description
    description = profile.find(class_='p-note user-profile-bio js-user-profile-bio mb-3').get_text()

    # Get the location
    location = profile.find(itemprop='homeLocation').get_text()

    # Get the followers and following
    nav_container = profile.find(class_='UnderlineNav user-profile-nav js-sticky top-0')
    followers = nav_container.find_all(class_='Counter')[3].get_text()
    following = nav_container.find_all(class_='Counter')[4].get_text()

    # Get the contribution activity
    contribution = profile.find(class_='f4 text-normal mb-2').get_text()

    # Get all the repositories on the first page
    repositories = repos.find_all(itemprop='owns')

    return [profile_img, repositories, contribution, name, username, followers.lstrip(), following.lstrip(), description, location]


def download_image(url):
    name = 'profile-image'
    fullname = str(name)+".jpg"
    urllib.request.urlretrieve(url, 'img/' + fullname)


def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    data = format_req_data()

    # Formdat data
    profile_img = data[0]
    repositories = data[1]
    contribution = data[2]
    name = data[3]
    username= data[4]
    followers = data[5]
    following = data[6]
    description = data[7]
    location = data[8]

    # Download profile image
    download_image(profile_img)

    # Add layout-image to the page
    pdf.image('img/layout-pdf.jpg', x=0, y=0, w=210)

    # Add profile-image to the page
    pdf.image('img/profile-image.jpg', x=18, y=8, w=81, link=profile_img)

    # Add name
    pdf.x = 110
    pdf.y = 6
    pdf.set_font('Arial', 'B', 22)
    pdf.multi_cell(80, 10, name, 0, 'L')

    # Add username
    pdf.x = 110
    pdf.y = 14
    pdf.set_font('Arial', '', 18)
    pdf.multi_cell(80, 10, username, 0, 'L')

    # Add the description
    pdf.x = 110
    pdf.y = 30
    pdf.set_font('Arial', 'I', 12)
    pdf.multi_cell(62, 10, description, 0, 'L')

    # Add the location
    pdf.x = 110
    pdf.y = 34
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(62, 10, location, 0, 'L')

    # Add github-logo
    pdf.image('img/github-logo.png', x=113, y=64, w=5, link=url_profile)
    # Add git link (string)
    pdf.x = 118
    pdf.y = 62
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(50, 10, '/ ' + username, 0, 'L')

    # Add followers button
    pdf.image('img/button.png', x=107, y=73, w=45, h=22, link=url_followers)
    # Add followers count
    pdf.x = 112
    pdf.y = 79.5
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(37, 10, 'Followers: ' + followers, 0, 'C')

    # Add following button
    pdf.image('img/button.png', x=152, y=73, w=45, h=22, link=url_following)
    # Add followeing count
    pdf.x = 156
    pdf.y = 79.5
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(37, 10, 'Following: ' + following, 0, 'C')

    # Add 'Repositories' heading
    pdf.y = 120
    pdf.x = 22
    repository_y = pdf.y
    pdf.set_font('Arial', 'B', 18)
    pdf.multi_cell(50, 10, 'Repositories', 0, 'L')

    # Define space between the first repository paragraph and the 'Repositories' heading
    space = 15

    for repository in repositories:
        # Repository title
        title = str(repository.find(itemprop='name codeRepository').get_text())

        # Add the title
        pdf.x = 22
        pdf.y = repository_y + space
        title_y = pdf.y
        pdf.set_font('Arial','', 14)
        pdf.multi_cell(70, 10, title.lstrip(), 0, 'L')
        space += 15

    # Add 'Contribution' heading
    pdf.x = 115
    pdf.y = 120
    pdf.set_font('Arial', 'B', 18)
    pdf.multi_cell(50, 10, 'Contribution', 0, 'L')

    file_name = 'Github-Profile-(' + name + ').pdf'

    # Save the file (add profile name)
    pdf.output(file_name)

    # Open the created file
    webbrowser.open_new(file_name)

create_pdf()
