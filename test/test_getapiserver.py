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

class TestGetApiServer(NoAuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testDefault(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'binapi': ['bineapi.pcloud.com'],
            'api'   : ['eapi.pcloud.com'],
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            servers = pCloud.getApiServer()

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
        self.assertEqual(servers, ['https://eapi.pcloud.com/'])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttp(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'binapi': ['bineapi.pcloud.com'],
            'api'   : ['eapi.pcloud.com'],
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            servers = pCloud.getApiServer(False)

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
        self.assertEqual(servers, ['https://eapi.pcloud.com/'])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testBinary(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'binapi': ['bineapi.pcloud.com'],
            'api'   : ['eapi.pcloud.com'],
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            servers = pCloud.getApiServer(True)

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
        self.assertEqual(servers, ['https://bineapi.pcloud.com/'])

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
                servers = pCloud.getApiServer()

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                servers = pCloud.getApiServer()

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                servers = pCloud.getApiServer()

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
