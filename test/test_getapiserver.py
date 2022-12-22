import requests
import unittest

from .testcase_noauth import NoAuthTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestGetApiServer(NoAuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testDefault(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'binapi': ['bineapi.pcloud.com'],
            'api'   : ['eapi.pcloud.com'],
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            servers = pCloud.getApiServer()

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
        self.assertEqual(servers, ['https://eapi.pcloud.com/'])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttp(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'binapi': ['bineapi.pcloud.com'],
            'api'   : ['eapi.pcloud.com'],
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            servers = pCloud.getApiServer(False)

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
        self.assertEqual(servers, ['https://eapi.pcloud.com/'])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testBinary(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'binapi': ['bineapi.pcloud.com'],
            'api'   : ['eapi.pcloud.com'],
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            servers = pCloud.getApiServer(True)

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
        self.assertEqual(servers, ['https://bineapi.pcloud.com/'])

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
                servers = pCloud.getApiServer()

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                servers = pCloud.getApiServer()

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                servers = pCloud.getApiServer()

        self.checkMock('GET', 'https://pcloud.localhost/getapiserver')
