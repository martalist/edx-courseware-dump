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

==

You can change the file types that are downloaded by adding/removing lines from the FILE_TYPES constant.

Note that the main content (video.mp4) will be downloaded even if "mp4" is removed from the constant.

## Caching and existing files

The first time you download from a course the list of files/links will be cached/saved to a .pkl file. On subsequent downloads you can skip the time consuming process of scraping the course chapters.

Files that already exit (that have already been downloaded) should should not be downloaded a second time. 
