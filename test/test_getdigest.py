import requests
import unittest

from .testcase_noauth import NoAuthTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestGetDigest(NoAuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testNormal(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            digest = pCloud.getDigest()

        self.checkMock('GET', 'https://pcloud.localhost/getdigest')
        self.assertEqual(digest, 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(PCloudError) as e:
                digest = pCloud.getDigest()

        self.assertEqual(e.exception.code, result)
        self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/getdigest')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                digest = pCloud.getDigest()

        self.checkMock('GET', 'https://pcloud.localhost/getdigest')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                digest = pCloud.getDigest()

        self.checkMock('GET', 'https://pcloud.localhost/getdigest')
