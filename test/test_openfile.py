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

from .testcase_session import SessionTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestOpenFile(SessionTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testIdNormal(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1, 'flags': int(PCloud.FileOpenFlags.O_APPEND)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPathNormal(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile('/New file'):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'path': '/New file', 'flags': int(PCloud.FileOpenFlags.O_APPEND)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})


    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testIdTruncate(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1, flags=PCloud.FileOpenFlags.O_TRUNC):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1, 'flags': int(PCloud.FileOpenFlags.O_TRUNC.value | PCloud.FileOpenFlags.O_WRITE)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPathTruncate(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile('/New file', flags=PCloud.FileOpenFlags.O_TRUNC):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'path': '/New file', 'flags': int(PCloud.FileOpenFlags.O_TRUNC | PCloud.FileOpenFlags.O_WRITE)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testIdWrite(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1, flags=PCloud.FileOpenFlags.O_WRITE):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1, 'flags': int(PCloud.FileOpenFlags.O_APPEND | PCloud.FileOpenFlags.O_WRITE)})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPathWrite(self, mock_session, mock_request):
        self.setupMockNormal(mock_session, mock_request, {'result': 0, 'fd': 18, 'fileid': 1})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile('/New file', flags=PCloud.FileOpenFlags.O_WRITE):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'path': '/New file', 'flags': int(PCloud.FileOpenFlags.O_APPEND | PCloud.FileOpenFlags.O_WRITE)})
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
                with pCloud.openFile(1):
                    pass #pragma: no cover

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1})

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
                with pCloud.openFile(1):
                    pass #pragma: no cover

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1})

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

            with pCloud.openFile(1):
                pass

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testOpenHttpError(self, mock_session, mock_request):
        self.setupMockOpenHttpError(mock_session, mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                with pCloud.openFile(1):
                    pass #pragma: no cover

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1})

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

                with pCloud.openFile(1):
                    pass
        else:
            with self.assertWarns(UserWarning) as w:
                with PCloud('https://pcloud.localhost/') as pCloud:
                    pCloud.username = 'username'
                    pCloud.password = 'password'

                    with pCloud.openFile(1):
                        pass

                self.assertEqual(len(w.warnings), 1)
                self.assertTrue(str(w.warnings[0].message).startswith("Could not close file 18 due to exception:"))

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1})
        self.checkCloseMock('GET', 'https://pcloud.localhost/file_close', params={'fd': 18})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testConnectionError(self, mock_session, mock_request):
        self.setupMockConnectionError(mock_session, mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                with pCloud.openFile(1):
                    pass #pragma: no cover

        self.checkOpenMock('GET', 'https://pcloud.localhost/file_open', params={'fileid': 1})
