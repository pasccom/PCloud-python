import requests
import unittest
import unittest.mock

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestPCloud(unittest.TestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testContextManager(self, mock_request):
        with PCloud('https://pcloud.localhost/') as pCloud:
            pass

        mock_request.assert_not_called()

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testAutoServer(self, mock_request):
        mock_requestServer = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestServer.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestServer.json.return_value = {
            'result': 0,
            'binapi': ['binapi.pcloud.com'],
            'api'   : ['api.pcloud.com'],
        }

        mock_requestIp = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestIp.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestIp.json.return_value = {
            'result':  0,
            'ip':      '127.0.0.1',
            'country': 'fr',
        }
        mock_request.side_effect = [mock_requestServer, mock_requestIp]

        with PCloud() as pCloud:
            ip = pCloud.getIp()

        self.assertEqual(len(mock_request.call_args_list), 2)
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://eapi.pcloud.com/getapiserver')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://api.pcloud.com/getip')
        self.assertEqual(len(mock_request.call_args_list[1][1]), 0)

        self.assertEqual(ip, '127.0.0.1')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testAutoServerHttpError(self, mock_request):
        mock_requestServer = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestServer.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_requestIp = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestIp.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestIp.json.return_value = {
            'result':  0,
            'ip':      '127.0.0.1',
            'country': 'fr',
        }
        mock_request.side_effect = [mock_requestServer, mock_requestIp]

        with PCloud() as pCloud:
            ip = pCloud.getIp()

        self.assertEqual(len(mock_request.call_args_list), 2)
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://eapi.pcloud.com/getapiserver')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://eapi.pcloud.com/getip')
        self.assertEqual(len(mock_request.call_args_list[1][1]), 0)

        self.assertEqual(ip, '127.0.0.1')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testAutoServerConnectionError(self, mock_request):
        mock_requestIp = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestIp.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestIp.json.return_value = {
            'result':  0,
            'ip':      '127.0.0.1',
            'country': 'fr',
        }
        mock_request.side_effect = [requests.exceptions.ConnectionError, mock_requestIp]

        with PCloud() as pCloud:
            ip = pCloud.getIp()

        self.assertEqual(len(mock_request.call_args_list), 2)
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://eapi.pcloud.com/getapiserver')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://eapi.pcloud.com/getip')
        self.assertEqual(len(mock_request.call_args_list[1][1]), 0)

        self.assertEqual(ip, '127.0.0.1')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testAuth(self, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_userInfo = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_userInfo.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_userInfo.json.return_value = {
            'result':    0,
            'auth': 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.side_effect = [mock_requestdigest, mock_userInfo, mock_logout]

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            info = pCloud.userInfo()
            self.assertTrue(pCloud.authenticated)

        self.assertEqual(len(mock_request.call_args_list), 3)
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://pcloud.localhost/getdigest')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://pcloud.localhost/userinfo')
        self.assertIn('params', mock_request.call_args_list[1][1])
        self.assertIn('username', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['username'], 'username')
        self.assertIn('digest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['digest'], 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')
        self.assertIn('passworddigest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['passworddigest'], 'e9d9e70ff0e5e360841217316d1161767819dd96')
        self.assertIn('getauth', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['getauth'], 1)
        self.assertIn('logout', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['logout'], 1)

        self.assertEqual(len(mock_request.call_args_list[2]), 2)
        self.assertEqual(len(mock_request.call_args_list[2][0]), 2)
        self.assertEqual(mock_request.call_args_list[2][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[2][0][1], 'https://pcloud.localhost/logout')
        self.assertIn('params', mock_request.call_args_list[2][1])
        self.assertIn('auth', mock_request.call_args_list[2][1]['params'])
        self.assertEqual(mock_request.call_args_list[2][1]['params']['auth'], 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth')

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testAuthError(self, mock_request, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_userInfo = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_userInfo.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_userInfo.json.return_value = {
            'result': result,
            'error' : error,
        }
        mock_request.side_effect = [mock_requestdigest, mock_userInfo]

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                digest = pCloud.userInfo()

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

            self.assertFalse(pCloud.authenticated)

        self.assertEqual(len(mock_request.call_args_list), 2)
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://pcloud.localhost/getdigest')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://pcloud.localhost/userinfo')
        self.assertIn('params', mock_request.call_args_list[1][1])
        self.assertIn('username', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['username'], 'username')
        self.assertIn('digest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['digest'], 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')
        self.assertIn('passworddigest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['passworddigest'], 'e9d9e70ff0e5e360841217316d1161767819dd96')
        self.assertIn('getauth', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['getauth'], 1)
        self.assertIn('logout', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['logout'], 1)

    @testdata.TestData([1, 2, 3])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testLogoutFail(self, failNumber, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_userInfo = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_userInfo.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_userInfo.json.return_value = {
            'result':    0,
            'auth': 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_logout_fail = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout_fail.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout_fail.json.return_value = {
            'result':    0,
            'auth_deleted': False,
        }
        return_values = [mock_requestdigest, mock_userInfo] + [mock_logout_fail] * failNumber
        if (failNumber < 3):
            return_values += [mock_logout]
        mock_request.side_effect = return_values

        if (failNumber < 3):
            with PCloud('https://pcloud.localhost/') as pCloud:
                pCloud.username = 'username'
                pCloud.password = 'password'

                info = pCloud.userInfo()
                self.assertTrue(pCloud.authenticated)
        else:
            with self.assertWarns(UserWarning) as w:
                with PCloud('https://pcloud.localhost/') as pCloud:
                    pCloud.username = 'username'
                    pCloud.password = 'password'

                    info = pCloud.userInfo()
                    self.assertTrue(pCloud.authenticated)

                self.assertEqual(len(w.warnings), 1)
                self.assertEqual(str(w.warnings[0].message), "Could not logout")

        self.assertEqual(len(mock_request.call_args_list), 2 + min([failNumber + 1, 3]))
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://pcloud.localhost/getdigest')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://pcloud.localhost/userinfo')
        self.assertIn('params', mock_request.call_args_list[1][1])
        self.assertIn('username', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['username'], 'username')
        self.assertIn('digest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['digest'], 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')
        self.assertIn('passworddigest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['passworddigest'], 'e9d9e70ff0e5e360841217316d1161767819dd96')
        self.assertIn('getauth', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['getauth'], 1)
        self.assertIn('logout', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['logout'], 1)

        for f in range(0, min(failNumber + 1, 3)):
            self.assertEqual(len(mock_request.call_args_list[2 + f]), 2)
            self.assertEqual(len(mock_request.call_args_list[2 + f][0]), 2)
            self.assertEqual(mock_request.call_args_list[2 + f][0][0], 'GET')
            self.assertEqual(mock_request.call_args_list[2 + f][0][1], 'https://pcloud.localhost/logout')
            self.assertIn('params', mock_request.call_args_list[2 + f][1])
            self.assertIn('auth', mock_request.call_args_list[2 + f][1]['params'])
            self.assertEqual(mock_request.call_args_list[2 + f][1]['params']['auth'], 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth')

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testLogoutError(self, mock_request, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_userInfo = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_userInfo.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_userInfo.json.return_value = {
            'result':    0,
            'auth': 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result': result,
            'error' : error,
        }
        return_values = [mock_requestdigest, mock_userInfo, mock_logout]
        mock_request.side_effect = return_values

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            info = pCloud.userInfo()
            self.assertTrue(pCloud.authenticated)

        self.assertEqual(len(mock_request.call_args_list), 3)
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://pcloud.localhost/getdigest')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://pcloud.localhost/userinfo')
        self.assertIn('params', mock_request.call_args_list[1][1])
        self.assertIn('username', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['username'], 'username')
        self.assertIn('digest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['digest'], 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')
        self.assertIn('passworddigest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['passworddigest'], 'e9d9e70ff0e5e360841217316d1161767819dd96')
        self.assertIn('getauth', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['getauth'], 1)
        self.assertIn('logout', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['logout'], 1)

        self.assertEqual(len(mock_request.call_args_list[2]), 2)
        self.assertEqual(len(mock_request.call_args_list[2][0]), 2)
        self.assertEqual(mock_request.call_args_list[2][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[2][0][1], 'https://pcloud.localhost/logout')
        self.assertIn('params', mock_request.call_args_list[2][1])
        self.assertIn('auth', mock_request.call_args_list[2][1]['params'])
        self.assertEqual(mock_request.call_args_list[2][1]['params']['auth'], 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth')

    @testdata.TestData([1, 2, 3])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testLogoutHttpError(self, failNumber, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_userInfo = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_userInfo.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_userInfo.json.return_value = {
            'result':    0,
            'auth': 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_logout_fail = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout_fail.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout_fail.raise_for_status.side_effect = requests.exceptions.HTTPError
        return_values = [mock_requestdigest, mock_userInfo] + [mock_logout_fail] * failNumber
        if (failNumber < 3):
            return_values += [mock_logout]
        mock_request.side_effect = return_values

        if (failNumber < 3):
            with PCloud('https://pcloud.localhost/') as pCloud:
                pCloud.username = 'username'
                pCloud.password = 'password'

                info = pCloud.userInfo()
                self.assertTrue(pCloud.authenticated)
        else:
            with self.assertWarns(UserWarning) as w:
                with PCloud('https://pcloud.localhost/') as pCloud:
                    pCloud.username = 'username'
                    pCloud.password = 'password'

                    info = pCloud.userInfo()
                    self.assertTrue(pCloud.authenticated)

                self.assertEqual(len(w.warnings), 1)
                self.assertTrue(str(w.warnings[0].message).startswith("Could not logout due to exception"))

        self.assertEqual(len(mock_request.call_args_list), 2 + min([failNumber + 1, 3]))
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://pcloud.localhost/getdigest')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://pcloud.localhost/userinfo')
        self.assertIn('params', mock_request.call_args_list[1][1])
        self.assertIn('username', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['username'], 'username')
        self.assertIn('digest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['digest'], 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')
        self.assertIn('passworddigest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['passworddigest'], 'e9d9e70ff0e5e360841217316d1161767819dd96')
        self.assertIn('getauth', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['getauth'], 1)
        self.assertIn('logout', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['logout'], 1)

        for f in range(0, min(failNumber + 1, 3)):
            self.assertEqual(len(mock_request.call_args_list[2 + f]), 2)
            self.assertEqual(len(mock_request.call_args_list[2 + f][0]), 2)
            self.assertEqual(mock_request.call_args_list[2 + f][0][0], 'GET')
            self.assertEqual(mock_request.call_args_list[2 + f][0][1], 'https://pcloud.localhost/logout')
            self.assertIn('params', mock_request.call_args_list[2 + f][1])
            self.assertIn('auth', mock_request.call_args_list[2 + f][1]['params'])
            self.assertEqual(mock_request.call_args_list[2 + f][1]['params']['auth'], 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth')

    @testdata.TestData([1, 2, 3])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testLogoutConnectionError(self, failNumber, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_userInfo = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_userInfo.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_userInfo.json.return_value = {
            'result':    0,
            'auth': 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        return_values = [mock_requestdigest, mock_userInfo] + [requests.exceptions.ConnectionError] * failNumber
        if (failNumber < 3):
            return_values += [mock_logout]
        mock_request.side_effect = return_values

        if (failNumber < 3):
            with PCloud('https://pcloud.localhost/') as pCloud:
                pCloud.username = 'username'
                pCloud.password = 'password'

                info = pCloud.userInfo()
                self.assertTrue(pCloud.authenticated)
        else:
            with self.assertWarns(UserWarning) as w:
                with PCloud('https://pcloud.localhost/') as pCloud:
                    pCloud.username = 'username'
                    pCloud.password = 'password'

                    info = pCloud.userInfo()
                    self.assertTrue(pCloud.authenticated)

                self.assertEqual(len(w.warnings), 1)
                self.assertTrue(str(w.warnings[0].message).startswith("Could not logout due to exception"))

        self.assertEqual(len(mock_request.call_args_list), 2 + min([failNumber + 1, 3]))
        self.assertEqual(len(mock_request.call_args_list[0]), 2)
        self.assertEqual(len(mock_request.call_args_list[0][0]), 2)
        self.assertEqual(mock_request.call_args_list[0][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[0][0][1], 'https://pcloud.localhost/getdigest')
        self.assertEqual(len(mock_request.call_args_list[0][1]), 0)

        self.assertEqual(len(mock_request.call_args_list[1]), 2)
        self.assertEqual(len(mock_request.call_args_list[1][0]), 2)
        self.assertEqual(mock_request.call_args_list[1][0][0], 'GET')
        self.assertEqual(mock_request.call_args_list[1][0][1], 'https://pcloud.localhost/userinfo')
        self.assertIn('params', mock_request.call_args_list[1][1])
        self.assertIn('username', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['username'], 'username')
        self.assertIn('digest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['digest'], 'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest')
        self.assertIn('passworddigest', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['passworddigest'], 'e9d9e70ff0e5e360841217316d1161767819dd96')
        self.assertIn('getauth', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['getauth'], 1)
        self.assertIn('logout', mock_request.call_args_list[1][1]['params'])
        self.assertEqual(mock_request.call_args_list[1][1]['params']['logout'], 1)

        for f in range(0, min(failNumber + 1, 3)):
            self.assertEqual(len(mock_request.call_args_list[2 + f]), 2)
            self.assertEqual(len(mock_request.call_args_list[2 + f][0]), 2)
            self.assertEqual(mock_request.call_args_list[2 + f][0][0], 'GET')
            self.assertEqual(mock_request.call_args_list[2 + f][0][1], 'https://pcloud.localhost/logout')
            self.assertIn('params', mock_request.call_args_list[2 + f][1])
            self.assertIn('auth', mock_request.call_args_list[2 + f][1]['params'])
            self.assertEqual(mock_request.call_args_list[2 + f][1]['params']['auth'], 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth')
