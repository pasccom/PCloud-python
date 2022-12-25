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

class TestCreateFolder(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdDefault(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder', [], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.createFolder(0, 'New folder')

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'folderid': 0, 'name': 'New folder'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathDefault(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New folder'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.createFolder('/', 'New folder')

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'path': '/New folder'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNotExists(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder', [], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.createFolder(0, 'New folder', exists=False)

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'folderid': 0, 'name': 'New folder'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNotExists(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder', [], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New folder'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.createFolder('/', 'New folder', exists=False)

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'path': '/New folder'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdExists(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder', [], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.createFolder(0, 'New folder', exists=True)

        self.checkMock('GET', 'https://pcloud.localhost/createfolder', params={'folderid': 0, 'name': 'New folder'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathExists(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New folder'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.createFolder('/', 'New folder', exists=True)

        self.checkMock('GET', 'https://pcloud.localhost/createfolder', params={'path': '/New folder'})
        root.check(self, folder)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudLoginErrorNotExists(self, mock_request, result, error):
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=False)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'folderid': 0, 'name': 'New folder'})

    @testdata.TestData([
        {'result': 1001, 'error': "No full path or name/folderid provided."                              },
        {'result': 2001, 'error': "Invalid file/folder name."                                            },
        {'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudErrorNotExists(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=False)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'folderid': 0, 'name': 'New folder'})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpErrorNotExists(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=False)

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'folderid': 0, 'name': 'New folder'})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionErrorNotExists(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=False)

        self.checkMock('GET', 'https://pcloud.localhost/createfolderifnotexists', params={'folderid': 0, 'name': 'New folder'})

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudLoginErrorExists(self, mock_request, result, error):
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=True)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/createfolder', params={'folderid': 0, 'name': 'New folder'})

    @testdata.TestData([
        {'result': 1001, 'error': "No full path or name/folderid provided."                              },
        {'result': 2001, 'error': "Invalid file/folder name."                                            },
        {'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2004, 'error': "File or folder alredy exists."                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudErrorExists(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=True)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/createfolder', params={'folderid': 0, 'name': 'New folder'})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpErrorExists(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=True)

        self.checkMock('GET', 'https://pcloud.localhost/createfolder', params={'folderid': 0, 'name': 'New folder'})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionErrorExists(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.createFolder(0, 'New folder', exists=True)

        self.checkMock('GET', 'https://pcloud.localhost/createfolder', params={'folderid': 0, 'name': 'New folder'})
