import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata


class TestCheck(AuthTestCase):
    checksums = {
        'sha256' : '7e5eccf073da87d63139a71899f25529d6029a73b5fd7390aec561a607d723ea',
        'sha1'   : '11d52a479a6366103a619ed762383a95cda9e27c',
        'md5'    : 'fa029a7f2a3ca5a03fe682d3b77c7f0d',
    }

    def __setChecksums(self, data):
        for k, v in TestCheck.checksums.items():
            if (k in data) and data[k]:
                data[k] = v
            elif (k in data):
                del(data[k])
        return data

    def checkMockSleep(self, mock_sleep, retry):
        self.assertEqual(len(mock_sleep.call_args_list), retry)
        for c in mock_sleep.call_args_list:
            self.assertEqual(c[0], (5, ))

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoOneOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoOneOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoOneOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value]))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoOneOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value]))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoAllOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoAllOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoAllOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value]))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoAllOK(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value]))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoOneKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length, algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoOneKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length, algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoOneKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoOneKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoAllKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length, algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoAllKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length, algorithm))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoAllKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoAllKO(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length))

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoOneRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm, True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoOneRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm, True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoOneRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value], retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoOneRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value], retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoAllRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm, True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoAllRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm, True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoAllRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check(1, TestCheck.checksums[algorithm.value], retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoAllRetryOK(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertTrue(pCloud.check('/New file', TestCheck.checksums[algorithm.value], retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoOneRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length, algorithm, True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoOneRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length, algorithm, True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoOneRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length, retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoOneRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length, retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoAllRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length, algorithm, retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoAllRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length, algorithm, retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoAllRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check(1, '0'*algorithm.length, retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'retry': 5},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 1},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 2},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 3},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 4},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'retry': 5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoAllRetryKO(self, mock_request, mock_sleep, algorithm, retry):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, retry, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            self.assertFalse(pCloud.check('/New file', '0'*algorithm.length, retry=True))

        self.checkMockRetry(retry, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, retry)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoOneRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm, True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoOneRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm, True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoOneRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], retry=True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoOneRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': (algorithm == PCloud.HashAlgorithm.SHA256),
            'sha1':   (algorithm == PCloud.HashAlgorithm.SHA1),
            'md5':    (algorithm == PCloud.HashAlgorithm.MD5),
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], retry=True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoAllRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm, True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoAllRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm, True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoAllRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], retry=True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.time.sleep')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoAllRetryFail(self, mock_request, mock_sleep, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockRetry(mock_request, 6, self.__setChecksums({
            'result': 0,
            'sha256': True,
            'sha1':   True,
            'md5':    True,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], retry=True)

            self.assertEqual(e.exception.code, 2009)
            self.assertEqual(str(e.exception), f"File not found (2009)")

        self.checkMockRetry(6, 'GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.checkMockSleep(mock_sleep, 5)

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoLoginError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoLoginError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value])

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 5000, 'error': "Internal error, try again later."          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1000, 'error': "Log in required."                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2000, 'error': "Log in failed."                            },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 4000, 'error': "Too many login tries from this IP address."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoLoginError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value])

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2010, 'error': "Invalid path."                                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2010, 'error': "Invalid path."                                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2010, 'error': "Invalid path."                                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value])

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA256, 'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.SHA1,   'result': 2010, 'error': "Invalid path."                                                        },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 1004, 'error': "No fileid or path provided."                                          },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2009, 'error': "File not found."                                                      },
        {'algorithm': PCloud.HashAlgorithm.MD5,    'result': 2010, 'error': "Invalid path."                                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoError(self, mock_request, algorithm, result, error):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value])

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoHttpError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoHttpError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoHttpError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value])

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoHttpError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value])

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgoConnectionError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value], algorithm)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgoConnectionError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value], algorithm)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNoAlgoAllConnectionError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                pCloud.check(1, TestCheck.checksums[algorithm.value])

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'algorithm': PCloud.HashAlgorithm.SHA256},
        {'algorithm': PCloud.HashAlgorithm.SHA1},
        {'algorithm': PCloud.HashAlgorithm.MD5},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNoAlgoConnectionError(self, mock_request, algorithm):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                pCloud.check('/New file', TestCheck.checksums[algorithm.value])

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
