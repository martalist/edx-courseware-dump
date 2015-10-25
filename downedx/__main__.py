#!/usr/bin/env python3

import os, sys, pickle
from getpass import getpass as gpass

from downedx import run
from dl_list import DownloadList

saved_list = None
dirfiles = os.listdir(os.getcwd())

# collect argument from the command line
if len(sys.argv) < 2:
    email = input("Enter your edX account email: ")
    password = gpass("Enter your edX password: ")
    url = DownloadList.check_url(input("Course url: "))
else:
    email = sys.argv[1]
    password = sys.argv[2]
    url = DownloadList.check_url(sys.argv[3])

# load cached/pickled dl_link lists
pkl_files = [x for x in dirfiles if x.endswith('.pkl')]
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

# push the red button
run(email, password, url, saved_list)
