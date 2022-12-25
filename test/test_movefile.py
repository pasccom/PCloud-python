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

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestMoveFile(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNormal(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test2', [PCloudTestFile('Test1', 1)], 2)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.moveFile(1, 2)

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 1, 'tofolderid': 2})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file')])])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/Test/New file'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.moveFile('/New file', '/Test')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'path': '/New file', 'topath': '/Test/'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath2(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New file')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New file'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.moveFile('/Test/New file', '/')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'path': '/Test/New file', 'topath': '/'})
        root.check(self, folder)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudLoginError(self, mock_request, result, error):
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.moveFile(1, 0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 1, 'tofolderid': 0})

    @testdata.TestData([
        {'result': 1004, 'error': "No fileid or path provided."                                          },
        {'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2009, 'error': "File not found."                                                      },
        {'result': 2010, 'error': "Invalid path."                                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.moveFile(1, 0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 1, 'tofolderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.moveFile(1, 0)

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 1, 'tofolderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.moveFile(1, 0)

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 1, 'tofolderid': 0})
