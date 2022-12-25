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

from .testcase import TestCase

class SessionTestCase(TestCase):
    def __init__(self, *args, **kwArgs):
        super().__init__(*args, **kwArgs)
        self.__mock = None
        self.__nCalls = None

    def setupMockNormal(self, mock_session, mock_request, return_value):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_open = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_open.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_open.json.return_value = return_value
        mock_open.json.return_value['auth'] = 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth'
        mock_close = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_close.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_close.json.return_value = {'result': 0}
        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, mock_open, mock_close]
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        self.__nCalls = 3

    def setupMockLoginError(self, mock_session, mock_request, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_open = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_open.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_open.json.return_value = {
            'result': result,
            'error' : error,
        }

        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, mock_open]
        mock_session.return_value = mock_session_object

        self.__mock = mock_session_object.request
        self.__nCalls = 2


    def setupMockOpenError(self, mock_session, mock_request, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_open = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_open.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_open.json.return_value = {
            'result': result,
            'error' : error,
            'auth'  : 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, mock_open]
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        self.__nCalls = 2

    def setupMockCloseError(self, mock_session, mock_request, fails, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_open = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_open.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_open.json.return_value = {
            'result': 0,
            'fd'    : 18,
            'fileid': 1,
            'auth'  : 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_close_failed = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_close_failed.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_close_failed.json.return_value = {
            'result': result,
            'error' : error,
        }
        mock_close = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_close.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_close.json.return_value = {'result': 0}
        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, mock_open, mock_close_failed]
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        self.__nCalls = 3

    def setupMockOpenHttpError(self, mock_session, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_open = unittest.mock.Mock(spec=requests.Response)
        mock_open.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, mock_open]
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        self.__nCalls = 2

    def setupMockCloseHttpError(self, mock_session, mock_request, fails):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_open = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_open.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_open.json.return_value = {
            'result': 0,
            'fd'    : 18,
            'fileid': 1,
            'auth'  : 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_close_failed = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_close_failed.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_close_failed.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_close = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_close.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_close.json.return_value = {'result': 0}
        mock_session_object = unittest.mock.Mock()
        if (fails < 3):
            mock_session_object.request.side_effect = [mock_requestdigest, mock_open] + [mock_close_failed]*fails + [mock_close]
        else:
            mock_session_object.request.side_effect = [mock_requestdigest, mock_open] + [mock_close_failed]*3
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        self.__nCalls = 2 + min(3, fails + 1)

    def setupMockConnectionError(self, mock_session, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, requests.exceptions.ConnectionError,]
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        self.__nCalls = 2

    def checkOpenMock(self, *args, **kwArgs):
        assert(self.__mock is not None)
        assert(self.__nCalls is not None)
        self.assertEqual(len(self.__mock.call_args_list), self.__nCalls)
        self.checkCall(self.__mock, 1, *args, **kwArgs)

    def checkCloseMock(self, *args, **kwArgs):
        assert(self.__mock is not None)
        assert(self.__nCalls is not None)
        self.assertEqual(len(self.__mock.call_args_list), self.__nCalls)
        for a in range(2, self.__nCalls):
            self.checkCall(self.__mock, a, *args, **kwArgs)
