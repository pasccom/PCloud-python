import requests
import unittest

from .testcase_file import FileTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestSeekFile(FileTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testNormal(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0, 'offset': 4})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                offset = pCloudFile.seek(4)

        self.checkMock('GET', 'https://pcloud.localhost/file_seek', params={'fd': 18, 'offset': 4, 'whence': 0})
        self.assertEqual(offset, 4)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testBegin(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0, 'offset': 4})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                offset = pCloudFile.seek(4, PCloud.OffsetOrigin.Begin)

        self.checkMock('GET', 'https://pcloud.localhost/file_seek', params={'fd': 18, 'offset': 4, 'whence': 0})
        self.assertEqual(offset, 4)


    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testCurrent(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0, 'offset': 8})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                offset = pCloudFile.seek(4, PCloud.OffsetOrigin.Current)

        self.checkMock('GET', 'https://pcloud.localhost/file_seek', params={'fd': 18, 'offset': 4, 'whence': 1})
        self.assertEqual(offset, 8)


    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testEnd(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0, 'offset': 12})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                offset = pCloudFile.seek(-4, PCloud.OffsetOrigin.End)

        self.checkMock('GET', 'https://pcloud.localhost/file_seek', params={'fd': 18, 'offset': -4, 'whence': 2})
        self.assertEqual(offset, 12)


    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 1007, 'error': "Invalid or closed file descriptor."        },
        {'result': 1009, 'error': "Please provide 'offset'."                  },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5004, 'error': "Read error, try reopening the file."       },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPCloudError(self, mock_session, mock_request, result, error):
        self.setupMock(mock_session, mock_request, 18, {'result': result, 'error': error})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(PCloudError) as e:
                    pCloudFile.seek(4)

                self.assertEqual(e.exception.code, result)
                self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/file_seek', params={'fd': 18, 'offset': 4, 'whence': 0})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testHttpError(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, requests.exceptions.HTTPError)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(requests.exceptions.HTTPError) as e:
                    pCloudFile.seek(4)

        self.checkMock('GET', 'https://pcloud.localhost/file_seek', params={'fd': 18, 'offset': 4, 'whence': 0})
