#!/usr/bin/env python3

import os, sys, pickle
from getpass import getpass as gpass

from downedx import run
from dl_list import DownloadList

saved_list = None
dirfiles = os.listdir(os.getcwd())

def load_cached_courses():
    pkl_files = [x for x in dirfiles if x.endswith('.pkl')]
    if len(pkl_files) > 0:
        for i, pkl_file in enumerate(pkl_files):
            with open(pkl_file, 'rb') as fh:
                pkl = pickle.load(fh)
                pkl_files[i] = pkl
    return pkl_files

def prompts(url=None):
    email = input("Enter your edX account email: ")
    password = gpass("Enter your edX password: ")
    if not url:
        url = DownloadList.check_url(input("Course url: "))
    return email, password, url


# load cached DownloadLists
pkl_files = load_cached_courses()

# collect argument from the command line
if len(sys.argv) > 1 and sys.argv[1] == 'history':
    for i, pkl in enumerate(pkl_files):
        print("{}. {}\t".format(i, pkl.course))
    while True:
        prompt = input('Enter the course number you\'d like to load, or "q" to quit: ')
        if int(prompt) in range(0, i+1) or prompt == 'q':
            break
    if prompt == 'q':
        sys.exit()
    else:
        email, password, url = prompts(pkl_files[int(prompt)].url)
        saved_list = pkl_files[int(prompt)]
else:
    if len(sys.argv) < 2:
        email, password, url = prompts()
    else:
        email, password, url = sys.argv[1:]

    # check cached DownloadLists
    for pkl in pkl_files:
        if url == pkl.url or DownloadList.course_name(url) == pkl.course:
            print("\nA list of download links already exits for this course."
                  "\nDo you want to use it?")
            prompt = None
            while prompt not in ['y', 'n']:
                prompt = input("    Enter 'y' if yes, 'n' if you'd like to scrape all links again: ")
                if prompt == 'y':
                    saved_list = pkl
            break

# push the red button
run(email, password, url, saved_list)
