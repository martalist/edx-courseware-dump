import datetime
import string


class DownloadList(list):

    def __init__(self, url):
        super(DownloadList, self).__init__()
        self.url = self.check_url(url)
        self.date = datetime.datetime.now()
        self.course = self.course_name(url)

    @staticmethod
    def check_url(url):
        url = url.split('/')
        if len(url) < 3 or any([
            url[0] != 'https:',
            url[2] != 'courses.edx.org',
            'courseware' not in url,
        ]):
            raise ValueError("\n\nPlease enter a valid edX url, pointing to the course's courseware section.\n")
        return '/'.join(url)

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
            course = DownloadList.replace_punctuation(course)
            return course
        return "unknown"

    @staticmethod
    def replace_punctuation(text):
        for i in string.punctuation:
            if i not in ['_', '-']:
                text = text.replace(i, '-')
        return text
