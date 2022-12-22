import requests
import unittest

from .testcase import TestCase

class FileTestCase(TestCase):
    def __init__(self, *args, **kwArgs):
        super().__init__(*args, **kwArgs)
        self.__mock = None
        self.__nCalls = None

    def __createResponse(self, return_value):
        mr = unittest.mock.Mock(spec=requests.Response, status_code=200)
        if type(return_value) is dict:
            mr.headers = {'Content-Type': 'application/json; charset=utf-8'}
            mr.json.return_value = return_value
        elif type(return_value) is bytes:
            mr.headers = {'Content-Type': 'application/octet-stream'}
            mr.content = return_value
        elif issubclass(return_value, BaseException):
            mr.raise_for_status.side_effect = return_value
        else:
            raise TypeError(f'Unsupported response type: {type(return_value)}')
        return mr

    def setupMock(self, mock_session, mock_request, fd, return_value):
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
            'fd'    : fd,
            'fileid': 1,
            'auth'  : 'AuthAuthAuthAuthAuthAuthAuthAuthAuthAuth',
        }
        if type(return_value) is list:
            mock_response = [self.__createResponse(rv) for rv in return_value]
        else:
            mock_response = [self.__createResponse(return_value)]
        mock_close = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_close.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_close.json.return_value = {'result': 0}
        mock_session_object = unittest.mock.Mock()
        mock_session_object.request.side_effect = [mock_requestdigest, mock_open] + mock_response + [mock_close]
        mock_session.return_value = mock_session_object

        mock_logout = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_logout.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_logout.json.return_value = {
            'result':    0,
            'auth_deleted': True,
        }
        mock_request.return_value = mock_logout

        self.__mock = mock_session_object.request
        if type(return_value) is list:
            self.__nCalls = 3 + len(return_value)
        else:
            self.__nCalls = 4
        self.__call = 2

    def checkMock(self, *args, **kwArgs):
        assert(self.__mock is not None)
        assert(self.__nCalls is not None)
        assert(self.__call is not None)
        assert(self.__call < self.__nCalls)

        self.checkCall(self.__mock, self.__call, *args, **kwArgs)
        self.__call += 1
