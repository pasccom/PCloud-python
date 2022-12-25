# Copyright 2022 Pascal COMBES <pascom@orange.fr>
#
# This file is part of PCloud-python.
#
# PCloud-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PCloud-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PCloud-python. If not, see <http://www.gnu.org/licenses/>

import requests
import unittest

from .testcase_noauth import NoAuthTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestSupportedLanguages(NoAuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testNormal(self, mock_request):
        expectedLanguages = {'de': 'Deutsch', 'en': 'English', 'fr': 'français', 'ru': 'Русский'}

        self.setupMockNormal(mock_request, {
            'result':    0,
            'languages': expectedLanguages,
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            languages = pCloud.supportedLanguages()

        self.checkMock('GET', 'https://pcloud.localhost/supportedlanguages')
        self.assertEqual(languages, expectedLanguages)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(PCloudError) as e:
                languages = pCloud.supportedLanguages()

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/supportedlanguages')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                languages = pCloud.supportedLanguages()

        self.checkMock('GET', 'https://pcloud.localhost/supportedlanguages')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                languages = pCloud.supportedLanguages()

        self.checkMock('GET', 'https://pcloud.localhost/supportedlanguages')
