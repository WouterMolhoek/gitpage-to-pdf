import urllib.request
from bs4 import BeautifulSoup
from fpdf import FPDF
import webbrowser

github_account = 'bufferbandit'
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
    if len(description) == 0:
        description = 'User has no description'
    else:
        description = (description.encode('ascii', 'ignore')).decode("utf-8").lstrip()

    # Get the location
    location = profile.find(itemprop='homeLocation')

    # Get the followers and following
    nav_container = profile.find(class_='UnderlineNav user-profile-nav js-sticky top-0')
    followers = nav_container.find_all(class_='Counter')[3].get_text().lstrip()
    following = nav_container.find_all(class_='Counter')[4].get_text().lstrip()

    # Get the contribution activity
    contribution = profile.find(class_='f4 text-normal mb-2').get_text()
    contribution = contribution.split(None, 1)[0]

    # Get the current month of activity
    month = profile.find(class_='profile-timeline-month-heading bg-white d-inline-block h6 pr-2 py-1').get_text().strip()

    created_details_container = profile.find(class_='profile-rollup-wrapper py-4 pl-4 position-relative ml-3 js-details-container Details open')
    # Get the created commits from the current month
    created_commits = created_details_container.find(class_='float-left').get_text().strip()
    created_commits = ' '.join(created_commits.split())

    # Get all the repositories on the first page, only get the first 8 items and the toal count of repositories
    repositories = repos.find_all(itemprop='owns')[:8]
    total_repositories = nav_container.find_all(class_='Counter')[0].get_text().strip()

    return (profile_img, repositories, contribution, name, username, followers, following, description, location, total_repositories, month, created_commits)


def download_image(url):
    file_name = 'profile-image.jpg'
    urllib.request.urlretrieve(url, f'img/{file_name}')


def create_pdf():
    pdf = FPDF()
    pdf.add_page()

    profile_img, repositories, contribution, name, username, followers, following, description, location, total_repositories, month, created_commits = format_req_data()

    # Download profile image
    download_image(profile_img)

    # Add layout-image to the page
    pdf.image('img/layout-pdf.jpg', x=0, y=0, w=210)

    # Add profile-image to the page
    pdf.image('img/profile-image.jpg', x=18, y=8, w=81, link=profile_img)

    # Add name
    pdf.x = 110
    pdf.y = 6.5
    pdf.set_font('Arial', 'B', 22)
    pdf.multi_cell(80, 10, name, 0, 'L')

    # Add username
    pdf.x = 110
    pdf.y = 14.5
    pdf.set_font('Arial', '', 18)
    pdf.multi_cell(80, 10, username, 0, 'L')

    # Add the description
    pdf.x = 110
    pdf.y = 28
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(75, 5, description, 0, 'L')

    # Add the location
    pdf.x = 110
    if location is None:
        location = 'User has no location'
    else:
        location = location.get_text()

    if len(description) > 140:
            pdf.y = 48
    else:
        pdf.y = 33

    pdf.set_font('Arial', 'I', 12)
    pdf.multi_cell(62, 10, str(location), 0, 'L')

    # Add github-logo
    if len(description) > 140:
        logo_y = 67
    else:
        logo_y = 61
    pdf.image('img/github-logo.png', x=112, y=logo_y + 2, w=5, link=url_profile)
    # Add git link (string)
    pdf.x = 117
    pdf.y = logo_y
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(50, 10, f'/ {username}', 0, 'L')

    # Add followers button
    pdf.image('img/button.png', x=107, y=73, w=45, h=22, link=url_followers)
    # Add followers count
    pdf.x = 112
    pdf.y = 79.5
    pdf.set_font('Arial', 'B', 11)
    pdf.multi_cell(37, 10, f'Followers: {followers}', 0, 'C')

    # Add following button
    pdf.image('img/button.png', x=152, y=73, w=45, h=22, link=url_following)
    # Add followeing count
    pdf.x = 156
    pdf.y = 79.5
    pdf.set_font('Arial', 'B', 11)
    pdf.multi_cell(37, 10, f'Following: {following}', 0, 'C')

    # Add 'Repositories' heading
    pdf.y = 120
    pdf.x = 22
    repository_y = pdf.y
    pdf.set_font('Arial', 'B', 18)
    pdf.multi_cell(75, 10, f'Repositories ({total_repositories})', 0, 'L')

    # Defines offset between the first repository paragraph and the 'Repositories' heading
    offset = 12

    for repository in repositories:
        # Repository title
        title = str(repository.find(itemprop='name codeRepository').get_text())

        # Add the title
        pdf.x = 22
        pdf.y = repository_y + offset
        title_y = pdf.y
        pdf.set_font('Arial','', 12)
        pdf.multi_cell(78, 10, f'- {title.lstrip()}', 0, 'L')
        offset += 15

    # Add 'Contribution' heading
    pdf.x = 115
    pdf.y = 120
    pdf.set_font('Arial', 'B', 18)
    pdf.multi_cell(50, 10, 'Contribution', 0, 'L')

    # Add contribution count
    pdf.x = 115
    pdf.y = 131
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(60, 10, f'{contribution} contributions last year', 0, 'L')

    # Add month contribution heading
    pdf.x = 115
    pdf.y = 163
    pdf.set_font('Arial', 'B', 18)
    pdf.multi_cell(50, 10, month, 0, 'L')

    # Add month contribution heading
    pdf.x = 115
    pdf.y = 175
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(50, 10, created_commits, 0, 'L')

    file_name = f'Github-Profile-({name}).pdf'

    # Save the file (add profile name)
    pdf.output(file_name)

    # Open the created file
    webbrowser.open_new(file_name)

create_pdf()
