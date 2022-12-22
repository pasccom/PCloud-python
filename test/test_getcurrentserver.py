import requests
import unittest

from .testcase_noauth import NoAuthTestCase

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestGetCurrentServer(NoAuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testNormal(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result':      0,
            'ip':          '45.131.244.9',
            'binhostname': 'bineapi3.pcloud.com',
            'hostname':    'eapi3.pcloud.com',
            'ipbin':       '45.131.244.39',
            'ipv6':        '::1',
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            server = pCloud.currentServer()

        self.checkMock('GET', 'https://pcloud.localhost/currentserver')
        self.assertEqual(server['ip'], '45.131.244.9')
        self.assertEqual(server['ipbin'], '45.131.244.39')
        self.assertEqual(server['ipv6'], '::1')
        self.assertEqual(server['hostname'], 'eapi3.pcloud.com')
        self.assertEqual(server['binhostname'], 'bineapi3.pcloud.com')
        self.assertNotIn('result', server)

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
                server = pCloud.currentServer()

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/currentserver')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.HTTPError) as e:
                server = pCloud.currentServer()

        self.checkMock('GET', 'https://pcloud.localhost/currentserver')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                server = pCloud.currentServer()

        self.checkMock('GET', 'https://pcloud.localhost/currentserver')
