import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestDeleteFolder(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNormal(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Old folder', [], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base=1))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.deleteFolder(1)

        self.checkMock('GET', 'https://pcloud.localhost/deletefolder', params={'folderid': 1})
        root.check(self, folder)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNormal(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Old folder')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': dict(root(base='/Old folder'))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            folder = pCloud.deleteFolder('/Old folder')

        self.checkMock('GET', 'https://pcloud.localhost/deletefolder', params={'path': '/Old folder'})
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
                folder = pCloud.deleteFolder(0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/deletefolder', params={'folderid': 0})

    @testdata.TestData([
        {'result': 1002, 'error': "No full path or folderid provided."                                   },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2005, 'error': "Directory does not exist."                                            },
        {'result': 2006, 'error': "Folder is not empty."                                                 },
        {'result': 2007, 'error': "Cannot delete the root folder."                                       },
        {'result': 2028, 'error': "There are active shares or sharerequests for this folder."            },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.deleteFolder(0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/deletefolder', params={'folderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.deleteFolder(0)

        self.checkMock('GET', 'https://pcloud.localhost/deletefolder', params={'folderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.deleteFolder(0)

        self.checkMock('GET', 'https://pcloud.localhost/deletefolder', params={'folderid': 0})
