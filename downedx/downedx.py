#!/usr/bin/env python3
import os, requests, pickle, sys
from bs4 import BeautifulSoup
from html import unescape
from pprint import pprint as pp

from dl_list import DownloadList

LOGIN_URL = 'https://courses.edx.org/user_api/v1/account/login_session/'
REFERRER = 'https://courses.edx.org/login'
FILE_TYPES = [
                '.pdf',
                '.zip',
                # '.srt',
                # '.torrent',
                '.mp4',
                '.py',
                # '.mp3',
                '.txt',
                ]


def edx_login(email, password):
    client = requests.Session()
    client.get(REFERRER)
    csrftoken = client.cookies['csrftoken']
    payload = {
        'action': 'login',
        'email': email,
        'password': password,
        'csrfmiddlewaretoken': csrftoken,
    }
    login = client.post(LOGIN_URL, data=payload, headers={'Referer': REFERRER})
    if login.status_code == requests.codes.forbidden:
        print('\nEmail or password is incorrect. Please try again with valid edX credentials.\n')
        sys.exit(1)
    return client


def fetch_course_html(client, url):
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
                    dl_list.append([chapter, subheading, 'section_{}'.format(i), link])
                    print('.', end='')
    if save:
        fn = os.path.join(os.getcwd(), dl_list.course + '_links.pkl')
        with open(fn, 'wb') as fh:
            pickle.dump(dl_list, fh)
    return dl_list


def mkdirs(link, dl_links):
    section = os.path.join(os.getcwd(), dl_links.course, link[0], link[1], link[2])
    if not os.path.exists(section):
        os.makedirs(section)
    return section


def download(client, dl_links):
    existing = new = 0
    for link in dl_links:
        filename = os.path.split(link[3])[-1]
        if not filename.endswith(tuple(FILE_TYPES)): continue
        path = mkdirs(link, dl_links)
        if os.path.isfile(os.path.join(path, filename)):
            existing += 1
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
                new += 1
            except requests.exceptions.HTTPError:
                with open('error_log_{}.log'.format(dl_links.course), 'a') as log:
                    log.write('{},{},{},{}\n'.format(link[0], link[1], link[2], link[3]))
    print("\nFinished downloading!",
            "\n    {} files downloaded.".format(new),
            "\n    {} files already existed.\n".format(existing))


def run(email, password, url, saved_list=None):
    print("    logging in to edX...")
    client = edx_login(email, password)
    if not saved_list:
        print("    fetching course content list...")
        soup = fetch_course_html(client, url)

        print("    building menu-item links...")
        menu_links = build_menu_item_links(soup)

        print('    finding all downloadable content...')
        dl_links = find_all_download_links(client, menu_links, url)
    else:
        dl_links = saved_list
    # pp(dl_links)

    download(client, dl_links)
