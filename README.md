# edx-courseware-dump
Completed an edX course and want to download all the courseware? This program should help you with that.

## Requirements
- Python3
- requests
- beautifulsoup4

## How to use

1. Download / clone
2. Open terminal, and navigate to the package folder
3. Enter:

```
$ python3 downedx
```

You'll be prompted to enter your email/password for edX, and the url for your course. <b>Be sure to use the *courseware url.*</b>

Alternatively you can enter your email, password and url as arguments:

```
$ python3 downedx your@email.com yourpass https://courses.edx.org/path/to/courseware
```

A directory will be created in the pwd, with all courseware downloaded to chapter/section subfolders.
