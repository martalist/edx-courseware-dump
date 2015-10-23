#!/usr/bin/env python3
import sys
import requests
from getpass import getpass as gpass
from bs4 import BeautifulSoup
from pprint import pprint as pp

LOGIN_URL = 'https://courses.edx.org/user_api/v1/account/login_session/'
REFERRER = 'https://courses.edx.org/login'

url = 'https://courses.edx.org/courses/HarvardX/CS50x3/2015/courseware/cdf0594e6a80402bbe902bb107fd2976/'


def edx_login():
    client = requests.Session()
    client.get(REFERRER)
    csrftoken = client.cookies['csrftoken']
    payload = {
        'action': 'login',
        'email': email,
        'password': password,
        'csrfmiddlewaretoken': csrftoken,
    }
    client.post(LOGIN_URL, data=payload, headers={'Referer': REFERRER})
    return client


def fetch_course_html(client):
    r = client.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def build_menu_item_links(soup):
    link_map = {}

    chapters = soup.find_all("div", class_="chapter-content-container")
    for chapter in chapters:
        heading = chapter['id'].rstrip('-child')

        menu_items = {}
        items = chapter.find_all("div", class_="menu-item")
        for item in items:
            sh = item.p.text.strip().replace(' ', '_') # TODO: remove commas and other punctuation
            href = item.a['href']
            href = 'https://courses.edx.org/' + href if 'http' not in href else href
            href = 'http://www.example.com' # TODO: remove this line when ready for production!
            menu_items[sh] = href

        link_map[heading] = menu_items

    return link_map


def download():
    client = edx_login()
    soup = fetch_course_html(client)

    menu_links = build_menu_item_links(soup)
    pp(menu_links) # TODO: remove this when done with it


    # for link in menu_links.values():
    #     for sh, href in link.items():
    #         sh_r = client.get(href) # TODO: REQUIRES the client to be authenticated on edX
    #         sh_soup = BeautifulSoup(sh_r.text, 'html.parser')

            # make a dict of sequence-list links

    # visit each sequence-list link, and create a list of links to downloadable content

    """downloads"""
    # Assume downloads will be save to folders in the pwd
    # for link in lis-of-links:
        # if chapter/menu-item folder doesn't exit, create it/them
        # if file-to-be-downloaded exists:
            # continue
        # Download each piece of content to the appropriate folder
            # only allow max 1-3 concurrent downloads at once
    #
    # print "finished" when complete
    # also print progress to the console






if __name__ == '__main__':
    if len(sys.argv) < 2:
        # print("\n    You must provide 3 arguments: edx-email, edx-password, edx-course-url", '\n')
        # sys.exit()
        email = input("Enter your edX account email: ")
        password = gpass("Enter your edX password: ")
        url = input("Course url: ")
    else:
        email = sys.argv[1]
        password = sys.argv[2]
        url = sys.argv[3]

    download()
