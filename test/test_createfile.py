import requests
import unittest

from .testcase_session import SessionTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestCreateFile(SessionTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testIdNormal(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.createFile(0, 'New file'):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPathNormal(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.createFile('/', 'New file'):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'path': '/New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})


    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testIdTruncate(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.createFile('/Test', 'New file'):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'path': '/Test/New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPCloudLoginError(self, mock_session, mock_request, result, error):
        self.setupMockLoginError(mock_session, mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                with pCloud.createFile(0, 'New file'):
                    pass #pragma: no cover

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})


    @testdata.TestData([
        {'result': 1004, 'error': "No fileid or path provided."                                          },
        {'result': 1006, 'error': "Please provide flags."                                                },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 2009, 'error': "File not found."                                                      },
        {'result': 2010, 'error': "Invalid path."                                                        },
        {'result': 5001, 'error': "Internal upload error."                                               },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testOpenPCloudError(self, mock_session, mock_request, result, error):
        self.setupMockOpenError(mock_session, mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                with pCloud.createFile(0, 'New file'):
                    pass #pragma: no cover

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})


    @testdata.TestData([
        {'fails': 1},
        {'fails': 2},
        {'fails': 3},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testClosePCloudError(self, mock_session, mock_request, fails):
        self.setupMockCloseError(mock_session, mock_request, fails, 1007, "Invalid or closed file descriptor.")

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.createFile(0, 'New file'):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})

        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testOpenHttpError(self, mock_session, mock_request):
        self.setupMockOpenHttpError(mock_session, mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                with pCloud.createFile(0, 'New file'):
                    pass #pragma: no cover

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})


    @testdata.TestData([
        {'fails': 1},
        {'fails': 2},
        {'fails': 3},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testCloseHttpError(self, mock_session, mock_request, fails):
        self.setupMockCloseHttpError(mock_session, mock_request, fails)

        if (fails < 3):
            with PCloud('https://pcloud.localhost/') as pCloud:
                pCloud.username = 'username'
                pCloud.password = 'password'

                with pCloud.createFile(0, 'New file'):
                    pass
        else:
            with self.assertWarns(UserWarning) as w:
                with PCloud('https://pcloud.localhost/') as pCloud:
                    pCloud.username = 'username'
                    pCloud.password = 'password'

                    with pCloud.createFile(0, 'New file'):
                        pass

                self.assertEqual(len(w.warnings), 1)
                self.assertTrue(str(w.warnings[0].message).startswith("Could not close file 18 due to exception:"))

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})

        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testConnectionError(self, mock_session, mock_request):
        self.setupMockConnectionError(mock_session, mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                with pCloud.createFile(0, 'New file'):
                    pass #pragma: no cover

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'folderid': 0, 'name': 'New file', 'flags': int(PCloud.FileOpenFlags.O_WRITE | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL)})
