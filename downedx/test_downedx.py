#!/usr/bin/env python3

import unittest
import requests, bs4, string

import downedx
from dl_list import DownloadList

class TestConnection(unittest.TestCase):

    def test_edx_login(self):
        pass


class TestDownloadList(unittest.TestCase):

    def test_check_url(self):
        self.assertEqual('https://courses.edx.org/courses/course-v1:MITx+6.00.2x_4+3T2015/courseware/8d9a47872ed641a1ace050f1c1ba7ac7/',
                        DownloadList.check_url('https://courses.edx.org/courses/course-v1:MITx+6.00.2x_4+3T2015/courseware/8d9a47872ed641a1ace050f1c1ba7ac7/'))
        with self.assertRaises(ValueError):
            DownloadList.check_url('')
            DownloadList.check_url('http://example.com')

    def test_course_name(self):
        self.assertEqual('course-v1-MITx-6-00-2x_4-3T2015',
                        DownloadList.course_name('https://courses.edx.org/courses/course-v1:MITx+6.00.2x_4+3T2015/courseware/8d9a47872ed641a1ace050f1c1ba7ac7/'))


    def test_replace_punctuation(self):
        self.assertEqual(DownloadList.replace_punctuation(''), '')
        self.assertEqual(DownloadList.replace_punctuation('123'), '123')
        self.assertEqual(DownloadList.replace_punctuation(string.punctuation), '--------------------------_-----')

if __name__ == '__main__':
    unittest.main()
