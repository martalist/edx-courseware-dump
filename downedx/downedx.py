#!/usr/bin/env python3
import sys
import os
import requests
import pickle
from getpass import getpass as gpass
from bs4 import BeautifulSoup
from html import unescape
from pprint import pprint as pp

from dl_list import DownloadList

LOGIN_URL = 'https://courses.edx.org/user_api/v1/account/login_session/'
REFERRER = 'https://courses.edx.org/login'
FILE_TYPES = ['pdf',
            #   'srt',
            #   'torrent',
            #   'mp4',
            #   '.py',
            #   'mp3',
              'txt']


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
            subheading = item.p.text.strip().replace(' ', '_')
            subheading = DownloadList.replace_punctuation(subheading)
            href = item.a['href']
            href = 'https://courses.edx.org/' + href if 'http' not in href else href
            menu_items[subheading] = href

        link_map[heading] = menu_items

    return link_map



def find_all_download_links(client, menu_links, url, save=True):
    dl_list = DownloadList(url)
    for chapter, menu in menu_links.items():
        print('    scanning "{}"'.format(chapter))
        for subheading, href in menu.items():
            print('      in "{}"'.format(subheading))
            r = client.get(href)
            soup = BeautifulSoup(r.text, 'html.parser')

            # get the number of sections for this subheading (subheading)
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
                    dl_list.append([chapter, subheading, 'section_{}'.format(i), video[0]['href'], "main_content"])

                # Get all links in the section body area
                links = seq.find_all('a')
                for link in links:
                    link = link['href']
                    if link.endswith('.download'): link = link.rstrip('.download')
                    if link[:4] != 'http': link = 'https://courses.edx.org' + link
                    if link.endswith(tuple(FILE_TYPES)):
                        dl_list.append([chapter, subheading, 'section_{}'.format(i), link])
                        print('.', end='')
    if save:
        fn = os.path.join(os.getcwd(), dl_list.course + '_links.pkl')
        with open(fn, 'wb') as fh:
            pickle.dump(dl_list, fh)
    return dl_list


def mkdirs(link, dl_links):
    course = os.path.join(os.getcwd(), dl_links.course)
    chapter = os.path.join(course, link[0])
    subheading = os.path.join(chapter, link[1])
    section = os.path.join(chapter, link[2])
    if not os.path.exists(section):
        os.makedirs(section)
    return section


def download(client, dl_links):
    for i, link in enumerate(dl_links):
        path = mkdirs(link, dl_links)
        filename = '{}_{}'.format(i, os.path.split(link[3])[-1])
        if os.path.isfile(os.path.join(path, filename)): # needs testing
            continue
        else:
            try:
                print("    Downloading {}".format(filename))
                res = client.get(link[3])
                res.raise_for_status()
                print("    Saving {}\n".format(filename))
                with open(os.path.join(path, filename), 'wb') as dl_file:
                    for chunk in res.iter_content(100000):
                        dl_file.write(chunk)
            except:
                raise Exception("Something went wrong with the download :(")


def run(saved_list=None):
    print("    logging in to edX...")
    client = edx_login()
    if not saved_list:
        print("    fetching course content list...")
        soup = fetch_course_html(client)

        print("    building menu-item links...")
        menu_links = build_menu_item_links(soup)

        print('    finding all downloadable content...')
        dl_links = find_all_download_links(client, menu_links, url)
    else:
        dl_links = saved_list
    # pp(dl_links)

    download(client, dl_links)


if __name__ == '__main__':
    saved_list = None
    if len(sys.argv) < 2:
        email = input("Enter your edX account email: ")
        password = gpass("Enter your edX password: ")
        url = DownloadList.check_url(input("Course url: "))
    else:
        email = sys.argv[1]
        password = sys.argv[2]
        url = DownloadList.check_url(sys.argv[3])

    pkl_files = [x for x in os.listdir(os.getcwd()) if x.endswith('.pkl')]
    if len(pkl_files) > 0:
        for pkl_file in pkl_files:
            with open(pkl_file, 'rb') as fh:
                pkl = pickle.load(fh)
                if url == pkl.url:
                    print("\nA list of download links already exits for this course."
                          "\nDo you want to use it?")
                    prompt = None
                    while prompt not in ['y', 'n']:
                        prompt = input("    Enter 'y' if yes, 'n' if you'd like to scrape all links again: ")
                        if prompt == 'y':
                            saved_list = pkl
                    break
    run(saved_list)
