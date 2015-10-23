#!/usr/bin/env python3
import sys
import os
import requests
from getpass import getpass as gpass
from bs4 import BeautifulSoup
from html import unescape
from pprint import pprint as pp

LOGIN_URL = 'https://courses.edx.org/user_api/v1/account/login_session/'
REFERRER = 'https://courses.edx.org/login'
FILE_TYPES = ['pdf',
              'srt',
              'torrent',
            #   'mp4',
              '.py',
            #   'mp3',
              'download']

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
            # href = 'http://www.example.com' # TODO: remove this line when ready for production!
            menu_items[sh] = href

        link_map[heading] = menu_items

    return link_map


def find_all_download_links(client, menu_links):
    dl_list = []
    for chapter, menu in menu_links.items():
        print('    scanning "{}"'.format(chapter))
        for sh, href in menu.items():
            print('      in "{}"'.format(sh))
            r = client.get(href)
            soup = BeautifulSoup(r.text, 'html.parser')

            # get the number of sections for this sh (subheading)
            num_seq = len(soup.select('#sequence-list > li'))
            print("        {} sections".format(num_seq))

            # iterate through the sections to find links
            for i in range(num_seq):
                # unescape section contents to make it parseable by BeautifulSoup
                seq_contents = [unescape(x.text.replace("'", '')) for x in \
                                soup.select('#seq_contents_{}'.format(i))]
                seq = BeautifulSoup(seq_contents[0], 'html.parser')

                # If a video exists, add the link
                video = seq.select('.video-download-button > a')
                if len(video) >= 1:
                    dl_list.append([chapter, sh, 'section_{}'.format(i), video[0]['href']])

                # Get all links in the section body area
                links = seq.find_all('a')
                for link in links:
                    if link['href'].endswith(tuple(FILE_TYPES)):
                        dl_list.append([chapter, sh, 'section_{}'.format(i), link['href']])
                        print('.', end='')
                print("")
    return dl_list


def download(dl_links):
    pass

    # Assume downloads will be save to folders in the pwd
    # for link in lis-of-links:
        # if chapter/menu-item folder doesn't exit, create it/them
        # if file-to-be-downloaded exists:
            # continue
        # Download each piece of content to the appropriate folder
            # only allow max 1-3 concurrent downloads at once
    pass


def run():
    print("    logging in to edX...")
    client = edx_login()
    print("    fetching course content list...")
    soup = fetch_course_html(client)
    print("    building menu-item links...")
    menu_links = build_menu_item_links(soup)
    # pp(menu_links) # TODO: remove this when done with it
    print('    finding all downloadable content...')
    dl_links = find_all_download_links(client, menu_links)
    pp(dl_links)
    #
    # download(dl_links)


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

    run()
