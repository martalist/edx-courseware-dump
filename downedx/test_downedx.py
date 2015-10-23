#!/usr/bin/env python3

import unittest
import requests, bs4

import downedx

class TestConnection(unittest.TestCase):

    def test_request_successful(self):
        # self.assertEqual(downedx.r.status_code, 200)
        self.assertIn('edX', downedx.soup.title.string)
        self.assertIn('CS50', downedx.soup.title.string)



if __name__ == '__main__':
    unittest.main()
