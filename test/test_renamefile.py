import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestRenameFile(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNormal(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.renameFile(1, 'New file')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 1, 'toname': 'New file'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New file'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.renameFile('/Old file', 'New file')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'path': '/Old file', 'topath': '/New file'})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath2(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file')])])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/Test/New file'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.renameFile('/Test/Old file', 'New file')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'path': '/Test/Old file', 'topath': '/Test/New file'})
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
                folder = pCloud.renameFile(0, 'New file')

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 0, 'toname': 'New file'})

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
                folder = pCloud.renameFile(0, 'New file')

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 0, 'toname': 'New file'})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.renameFile(0, 'New file')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 0, 'toname': 'New file'})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.renameFile(0, 'New file')

        self.checkMock('GET', 'https://pcloud.localhost/renamefile', params={'fileid': 0, 'toname': 'New file'})
