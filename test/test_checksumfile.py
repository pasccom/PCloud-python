import requests
import unittest

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestChecksumFile(AuthTestCase):
    checksums = {
        'sha256' : '7e5eccf073da87d63139a71899f25529d6029a73b5fd7390aec561a607d723ea',
        'sha1'   : '11d52a479a6366103a619ed762383a95cda9e27c',
        'md5'    : 'fa029a7f2a3ca5a03fe682d3b77c7f0d',
    }

    def __setChecksums(self, data):
        for k, v in TestChecksumFile.checksums.items():
            if (k in data) and data[k]:
                data[k] = v
            elif (k in data):
                del(data[k])
        return data

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdNone(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {
            'result': 0,
            'metadata': dict(root(base=1))
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            checksum = pCloud.checksumFile(1)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        root.check(self, checksum)

    @testdata.TestData([
        {'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'sha256'},
        {'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha256'},
        {'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'sha256'},
        {'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdBest(self, mock_request, sha256, sha1, md5, expectation):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            checksum = pCloud.checksumFile(1)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.assertEqual(checksum, TestChecksumFile.checksums[expectation])

    @testdata.TestData([
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAlgo(self, mock_request, algo, sha256, sha1, md5, expectation):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            if (expectation != algo.value):
                with self.assertWarns(UserWarning) as w:
                    checksum = pCloud.checksumFile(1, algorithm=algo)

                self.assertEqual(len(w.warnings), 1)
                self.assertEqual(str(w.warnings[0].message), f"Could not find {algo.name} checksum. Returning best checksum")
            else:
                checksum = pCloud.checksumFile(1, algorithm=algo)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.assertEqual(checksum, TestChecksumFile.checksums[expectation])

    @testdata.TestData([
        {'sha256':  True, 'sha1':  True, 'md5':  True},
        {'sha256':  True, 'sha1':  True, 'md5': False},
        {'sha256':  True, 'sha1': False, 'md5':  True},
        {'sha256':  True, 'sha1': False, 'md5': False},
        {'sha256': False, 'sha1':  True, 'md5':  True},
        {'sha256': False, 'sha1':  True, 'md5': False},
        {'sha256': False, 'sha1': False, 'md5':  True},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdAll(self, mock_request, sha256, sha1, md5):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
            'metadata': dict(root(base=1))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            checksums = pCloud.checksumFile(1, PCloud.HashAlgorithm.ALL)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
        self.assertEqual(checksums, self.__setChecksums({
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
        }))

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathNone(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, {
            'result': 0,
            'metadata': dict(root(base='/New file'))
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            checksum = pCloud.checksumFile('/New file')

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        root.check(self, checksum)

    @testdata.TestData([
        {'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'sha256'},
        {'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha256'},
        {'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'sha256'},
        {'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathBest(self, mock_request, sha256, sha1, md5, expectation):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
            'metadata': dict(root(base='/New file'))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            checksum = pCloud.checksumFile('/New file')

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.assertEqual(checksum, TestChecksumFile.checksums[expectation])

    @testdata.TestData([
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA256, 'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.SHA1,   'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1':  True, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1':  True, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256':  True, 'sha1': False, 'md5': False, 'expectation': 'sha256'},
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256': False, 'sha1':  True, 'md5':  True, 'expectation': 'md5'   },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256': False, 'sha1':  True, 'md5': False, 'expectation': 'sha1'  },
        {'algo': PCloud.HashAlgorithm.MD5,    'sha256': False, 'sha1': False, 'md5':  True, 'expectation': 'md5'   },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAlgo(self, mock_request, algo, sha256, sha1, md5, expectation):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
            'metadata': dict(root(base='/New file'))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            if (expectation != algo.value):
                with self.assertWarns(UserWarning) as w:
                    checksum = pCloud.checksumFile('/New file', algorithm=algo)

                self.assertEqual(len(w.warnings), 1)
                self.assertEqual(str(w.warnings[0].message), f"Could not find {algo.name} checksum. Returning best checksum")
            else:
                checksum = pCloud.checksumFile('/New file', algorithm=algo)



        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.assertEqual(checksum, TestChecksumFile.checksums[expectation])

    @testdata.TestData([
        {'sha256':  True, 'sha1':  True, 'md5':  True},
        {'sha256':  True, 'sha1':  True, 'md5': False},
        {'sha256':  True, 'sha1': False, 'md5':  True},
        {'sha256':  True, 'sha1': False, 'md5': False},
        {'sha256': False, 'sha1':  True, 'md5':  True},
        {'sha256': False, 'sha1':  True, 'md5': False},
        {'sha256': False, 'sha1': False, 'md5':  True},
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathAll(self, mock_request, sha256, sha1, md5):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, self.__setChecksums({
            'result': 0,
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
            'metadata': dict(root(base='/New file'))
        }))

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            checksums = pCloud.checksumFile('/New file', PCloud.HashAlgorithm.ALL)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'path': '/New file'})
        self.assertEqual(checksums, self.__setChecksums({
            'sha256': sha256,
            'sha1':   sha1,
            'md5':    md5,
        }))

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                          },
        {'result': 2000, 'error': "Log in failed."                            },
        {'result': 4000, 'error': "Too many login tries from this IP address."},
        {'result': 5000, 'error': "Internal error, try again later."          },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudLoginError(self, mock_request, result, error):
        self.setupMockLoginError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.checksumFile(1)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @testdata.TestData([
        {'result': 1004, 'error': "No fileid or path provided."                                          },
        {'result': 2002, 'error': "A component of parent directory does not exist."                      },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2009, 'error': "File not found."                                                      },
        {'result': 2010, 'error': "Invalid path."                                                        },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                folder = pCloud.checksumFile(1)

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                folder = pCloud.checksumFile(1)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                folder = pCloud.checksumFile(1)

        self.checkMock('GET', 'https://pcloud.localhost/checksumfile', params={'fileid': 1})
