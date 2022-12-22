import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestListFolder(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def __testNormal(self, root, base, mock_request, recursive=False, noFiles=False):
        if recursive:
            self.setupMockNormal(mock_request, {'result' : 0, 'metadata': dict(root(base=base))})
        else:
            self.setupMockNormal(mock_request, {'result' : 0, 'metadata': dict(root(depth=1, base=base))})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            r = pCloud.listFolder(base, recursive=recursive, noFiles=noFiles)

        if type(base) is int:
            self.checkMock('GET', 'https://pcloud.localhost/listfolder', params={'folderid': base})
        elif type(base) is str:
            self.checkMock('GET', 'https://pcloud.localhost/listfolder', params={'path': base})
        else:
            raise TypeError(f"Invalid base type: {type(base)}")
        root.check(self, r)

    def testIdRootEmpty(self):
        self.__testNormal(PCloudTestRootFolder(), 0)

    def testPathRootEmpty(self):
        self.__testNormal(PCloudTestRootFolder(), '/')

    def testIdFile1(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFile('test')]), 0)

    def testIdFile2(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFile('test1'), PCloudTestFile('test2')]), 0)

    def testPathFile1(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFile('test')]), '/')

    def testPathFile2(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFile('test1'), PCloudTestFile('test2')]), '/')

    def testIdFolder1(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFolder('Test')]), 0)

    def testIdFolder2(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFolder('Test1'), PCloudTestFolder('Test2')]), 0)

    def testPathFolder1(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFolder('Test')]), '/')

    def testPathFolder2(self):
        self.__testNormal(PCloudTestRootFolder([PCloudTestFolder('Test1'), PCloudTestFolder('Test2')]), '/')

    def testIdTree1(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), 0)

    def testIdTree2(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), 0)

    def testPathTree1(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), '/')

    def testPathTree2(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), '/')

    def testIdTree1Recursive(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), 0, recursive=True)

    def testIdTree2Recursive(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), 0, recursive=True)

    def testPathTree1Recursive(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), '/', recursive=True)

    def testPathTree2Recursive(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), '/', recursive=True)

    def testIdTree1NotRoot(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')], 1)
        ]), 1)

    def testIdTree2NotRoot(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')], 1),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')], 2)
        ]), 1)

    def testPathTree1NotRoot(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), '/Test')

    def testPathTree2NotRoot(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), '/Test2')

    def testIdTree1NoFiles(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), 0, noFiles=True)

    def testIdTree2NoFiles(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), 0, noFiles=True)

    def testPathTree1NoFiles(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test', [PCloudTestFile('test')])
        ]), '/', noFiles=True)

    def testPathTree2NoFiles(self):
        self.__testNormal(PCloudTestRootFolder([
            PCloudTestFolder('Test1', [PCloudTestFile('test11'), PCloudTestFile('test12')]),
            PCloudTestFolder('Test2', [PCloudTestFile('test21'), PCloudTestFile('test22')])
        ]), '/', noFiles=True)

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
                folder = pCloud.listFolder(0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/listfolder', params={'folderid': 0})

    @testdata.TestData([
        {'result': 1002, 'error': "No full path or folderid provided."                                   },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2005, 'error': "Directory does not exist."                                            },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.listFolder(0)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/listfolder', params={'folderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.listFolder(0)

        self.checkMock('GET', 'https://pcloud.localhost/listfolder', params={'folderid': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.listFolder(0)

        self.checkMock('GET', 'https://pcloud.localhost/listfolder', params={'folderid': 0})
