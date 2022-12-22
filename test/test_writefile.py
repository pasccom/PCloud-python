import requests
import unittest

from .testcase_file import FileTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestWriteFile(FileTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testNormal(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0, 'bytes': 4})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                written = pCloudFile.write(b'Test')

        self.checkMock('PUT', 'https://pcloud.localhost/file_write', params={'fd': 18}, data=b'Test')
        self.assertEqual(written, 4)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testOffset(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, {'result': 0, 'bytes': 4})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                written = pCloudFile.write(b'Test', offset=36)

        self.checkMock('PUT', 'https://pcloud.localhost/file_pwrite', params={'fd': 18, 'offset': 36}, data=b'Test')
        self.assertEqual(written, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
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
                    pCloudFile.write(b'Test')

                self.assertEqual(e.exception.code, result)
                self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('PUT', 'https://pcloud.localhost/file_write', params={'fd': 18}, data=b'Test')

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testOffsetPCloudError(self, mock_session, mock_request, result, error):
        self.setupMock(mock_session, mock_request, 18, {'result': result, 'error': error})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(PCloudError) as e:
                    pCloudFile.write(b'Test', offset=36)

                self.assertEqual(e.exception.code, result)
                self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('PUT', 'https://pcloud.localhost/file_pwrite', params={'fd': 18, 'offset': 36}, data=b'Test')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testHttpError(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, requests.exceptions.HTTPError)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(requests.exceptions.HTTPError) as e:
                    pCloudFile.write(b'Test')

        self.checkMock('PUT', 'https://pcloud.localhost/file_write', params={'fd': 18}, data=b'Test')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def testOffsetHttpErrorOffset(self, mock_session, mock_request):
        self.setupMock(mock_session, mock_request, 18, requests.exceptions.HTTPError)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with pCloud.openFile(1) as pCloudFile:
                with self.assertRaises(requests.exceptions.HTTPError) as e:
                    pCloudFile.write(b'Test', offset=36)

        self.checkMock('PUT', 'https://pcloud.localhost/file_pwrite', params={'fd': 18, 'offset': 36}, data=b'Test')
