import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestMoveFolder(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNormal(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test2', [PCloudTestFolder('Test1', [], 1)], 2)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.moveFolder(1, 2)

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'folderid': 1, 'tofolderid': 2})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFolder('New folder')])])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/Test/New folder'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.moveFolder('/New folder', '/Test')

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'path': '/New folder', 'topath': '/Test/'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath2(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New folder')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New folder'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.moveFolder('/Test/New folder', '/')

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'path': '/Test/New folder', 'topath': '/'})
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
                folder = pCloud.moveFolder(1, 0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'folderid': 1, 'tofolderid': 0})

    @testdata.TestData([
        {'result': 1002, 'error': "No full path or folderid provided."                                   },
        {'result': 1017, 'error': "Invalid 'folderid' provided."                                         },
        {'result': 1037, 'error': "Please provide at least one of 'topath', 'tofolderid' or 'toname'."   },
        {'result': 2001, 'error': "Invalid file/folder name."                                            },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2004, 'error': "File or folder alredy exists."                                        },
        {'result': 2005, 'error': "Directory does not exist."                                            },
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 2023, 'error': "You are trying to place shared folder into another shared folder."    },
        {'result': 2043, 'error': "Cannot move a folder to a subfolder of itself."                       },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.moveFolder(1, 0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'folderid': 1, 'tofolderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.moveFolder(1, 0)

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'folderid': 1, 'tofolderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.moveFolder(1, 0)

        self.checkMock('GET', 'https://pcloud.localhost/renamefolder', params={'folderid': 1, 'tofolderid': 0})
