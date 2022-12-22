import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestCopyFile(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNormal(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test2', [PCloudTestFile('Test1', 1)], 2)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.copyFile(1, 2)

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 2, 'noover': True})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFolder('New file')])])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/Test/New file'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.copyFile('/New file', '/Test')

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'path': '/New file', 'topath': '/Test/',  'noover': True})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPath2(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('New file')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/New file'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.copyFile('/Test/New file', '/')

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'path': '/Test/New file', 'topath': '/', 'noover': True})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoOver(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test2', [PCloudTestFile('Test1', 1)], 2)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.copyFile(1, 2, overwrite=False)

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 2, 'noover': True})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdOver(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test2', [PCloudTestFile('Test1', 1)], 2)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.copyFile(1, 2, overwrite=True)

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 2, 'noover': False})
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
                folder = pCloud.copyFile(1, 0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 0})

    @testdata.TestData([
        {'result': 1004, 'error': "No fileid or path provided."                                          },
        {'result': 1016, 'error': "No full topath or toname/tofolderid provided."                        },
        {'result': 2001, 'error': "Invalid file/folder name."                                            },
        {'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2004, 'error': "File or folder alredy exists."                                        },
        {'result': 2008, 'error': "User is over quota."                                                  },
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
                folder = pCloud.copyFile(1, 0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.copyFile(1, 0)

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.copyFile(1, 0)

        self.checkMock('GET', 'https://pcloud.localhost/copyfile', params={'fileid': 1, 'tofolderid': 0})
