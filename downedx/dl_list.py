import datetime
import string


class DownloadList(list):

    def __init__(self, url):
        super(DownloadList, self).__init__()
        self.url = url
        self.date = datetime.datetime.now()
        self.course = self.course_name(url)

    @staticmethod
    def course_name(url):
        url = url.split('/')
        try:
            start = url.index('courses')
            stop = url.index('courseware')
        except ValueError:
            start = stop = None

        if start and stop:
            course = '_'.join(url[start + 1:stop])
            for i in string.punctuation:
                if i not in ['_', '-']:
                    course = course.replace(i, '-')
            return course
        return "unknown"
