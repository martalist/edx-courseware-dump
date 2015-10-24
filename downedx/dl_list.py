import datetime


class DownloadList(list):

    def __init__(self, url):
        super(DownloadList, self).__init__()
        self.url = url
        self.date = datetime.datetime.now()
