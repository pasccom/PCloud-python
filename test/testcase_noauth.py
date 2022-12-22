import requests
import unittest

from .testcase import TestCase

class NoAuthTestCase(TestCase):
    def __init__(self, *args, **kwArgs):
        super().__init__(*args, **kwArgs)
        self.__mock = None
        self.__nCalls = None

    def setupMockNormal(self, mock_request, return_value):
        mock_response = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_response.json.return_value = return_value
        mock_request.return_value = mock_response
        self.__mock = mock_request
        self.__nCalls = 1

    def setupMockError(self, mock_request, result, error):
        mock_response = unittest.mock.Mock(spec=requests.Response, status_code=200)
        mock_response.headers = {'Content-Type': 'application/json; charset=utf-8'}
        mock_response.json.return_value = {
            'result': result,
            'error' : error,
        }
        mock_request.return_value = mock_response
        self.__mock = mock_request
        self.__nCalls = 1

    def setupMockHttpError(self, mock_request):
        mock_response = unittest.mock.Mock(spec=requests.Response)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_request.return_value = mock_response
        self.__mock = mock_request
        self.__nCalls = 1

    def setupMockConnectionError(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError
        self.__mock = mock_request
        self.__nCalls = 1

    def checkMock(self, *args, **kwArgs):
        assert(self.__mock is not None)
        assert(self.__nCalls is not None)
        self.assertEqual(len(self.__mock.call_args_list), self.__nCalls)
        self.checkCall(self.__mock, 0, *args, **kwArgs)
