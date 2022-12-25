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

class AuthTestCase(TestCase):
    def __init__(self, *args, **kwArgs):
        super().__init__(*args, **kwArgs)
        self.__mock = None
        self.__nCalls = None

    def setupMockNormal(self, mock_request, return_value):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }

        mock_response = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_response.json.return_value = return_value
        mock_response.json.return_value['auth'] = 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth'

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.side_effect = [mock_requestdigest, mock_response, mock_logout]
        self.__mock = mock_request
        self.__nCalls = 3

    def setupMockRetry(self, mock_request, retry, return_value):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }

        mock_first_retry = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_first_retry.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_first_retry.json.return_value = {
            'result': 2009,
            'error': "File not found"
        }
        mock_first_retry.json.return_value['auth'] = 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth'

        mock_retry = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_retry.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_retry.json.return_value = {
            'result': 2009,
            'error': "File not found"
        }

        mock_response = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_response.json.return_value = return_value

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.side_effect = [mock_requestdigest, mock_first_retry] + [mock_retry]*(retry - 1) + [mock_response, mock_logout]
        self.__mock = mock_request
        self.__nCalls = 3 + retry

    def setupMockLoginError(self, mock_request, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_response = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_response.json.return_value = {
            'result': result,
            'error' : error,
        }
        mock_request.side_effect = [mock_requestdigest, mock_response]
        self.__mock = mock_request
        self.__nCalls = 2

    def setupMockError(self, mock_request, result, error):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_response = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_response.json.return_value = {
            'result': result,
            'error' : error,
            'auth'  : 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.side_effect = [mock_requestdigest, mock_response, mock_logout]
        self.__mock = mock_request
        self.__nCalls = 3

    def setupMockHttpError(self, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }

        mock_response = unittest.mock.Mock(spec=requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

        mock_request.side_effect = [mock_requestdigest, mock_response]
        self.__mock = mock_request
        self.__nCalls = 2

    def setupMockConnectionError(self, mock_request):
        mock_requestdigest = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_requestdigest.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_requestdigest.json.return_value = {
            'result':  0,
            'expires': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'digest':  'pCloudpCloudpCloudDigestDigestDigestDigestDigestDigestDigest'
        }
        mock_request.side_effect = [mock_requestdigest, requests.exceptions.ConnectionError]
        self.__mock = mock_request
        self.__nCalls = 2

    def checkMock(self, *args, **kwArgs):
        assert(self.__mock is not None)
        assert(self.__nCalls is not None)
        self.assertEqual(len(self.__mock.call_args_list), self.__nCalls)
        self.checkCall(self.__mock, 1, *args, **kwArgs)

    def checkMockRetry(self, retry, *args, **kwArgs):
        assert(self.__mock is not None)
        assert(self.__nCalls is not None)
        self.assertEqual(len(self.__mock.call_args_list), self.__nCalls)
        for r in range(0, min(retry + 1, 6)):
            self.checkCall(self.__mock, 1 + r, *args, **kwArgs)

