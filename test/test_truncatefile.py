import requests
import unittest

from .testcase_file import FileTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestTruncateFile(FileTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testNormal(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                pCloudFile.truncate(4)

        self.checkMock('GET', 'https://pcloud.localhost/file_truncate', params={'fd': 18, 'length': 4})

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 1007, 'error': "Invalid or closed file descriptor."        },
        {'result': 1010, 'error': "Please provide 'length'."                  },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5003, 'error': "Write error, try reopening the file."      },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testPCloud(self, mock_session, mock_request, result, error):
        self.setupMock(mock_session, mock_request, 18, {'result': result, 'error': error})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(PCloudError) as e:
                    pCloudFile.truncate(4)

                self.assertEqual(e.exception.code, result)
                self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/file_truncate', params={'fd': 18, 'length': 4})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testHttpError(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, requests.exceptions.HTTPError)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(requests.exceptions.HTTPError) as e:
                    pCloudFile.truncate(4)

        self.checkMock('GET', 'https://pcloud.localhost/file_truncate', params={'fd': 18, 'length': 4})
