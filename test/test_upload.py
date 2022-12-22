import requests
import unittest

from .testcase_file import FileTestCase

from pcloud import PCloud
from pcloud.src.file import PCloudFile
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestUpload(FileTestCase):
    @unittest.mock.patch('pcloud.src.main.os.remove')
    @unittest.mock.patch('pcloud.src.main.os.path.isfile')
    @unittest.mock.patch('pcloud.src.main.open')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def __testNormal(self, fileIdOrPath, data, prog, mock_session, mock_request, mock_open, mock_isfile, mock_remove):
        # Setup mocks
        maxProgress = (prog or 0) + sum([len(d) for d in data])
        self.setupMock(mock_session, mock_request, 18, [{'result': 0, 'bytes': len(d)} for d in data])

        dataFile = unittest.mock.MagicMock()
        dataFile.__enter__.return_value = dataFile
        dataFile.read.side_effect = data + [b'']

        progFile = unittest.mock.MagicMock()
        progFile.__enter__.return_value = progFile
        if prog is not None:
            progFile.read.side_effect = str(prog)

        unittest.mock.mock_open(mock_open)
        if prog is None:
            mock_open.side_effect = [dataFile] + [progFile]*(len(data) + 1)
        else:
            mock_open.side_effect = [progFile, dataFile] + [progFile]*(len(data) + 1)

        mock_isfile.return_value = prog is not None

        # Execute test
        PCloudFile.blockSize = 8
        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            expectedProgress = prog or 0
            for p in pCloud.upload('test.txt', fileIdOrPath):
                self.assertEqual(p, expectedProgress)
                expectedProgress = min(expectedProgress + PCloudFile.blockSize, maxProgress)

        # Check mocks
        for d in data:
            self.checkMock('PUT', 'https://pcloud.localhost/file_pwrite', params={'fd': 18}, data=d)

        if prog is not None:
            self.checkCall(mock_open, 0, 'test.txt.prog', 'rt')
            self.assertEqual([c[0] for c in progFile.read.call_args_list], [()])

        self.checkCall(mock_open, int(prog is not None), 'test.txt', 'rb')
        self.checkCall(dataFile.seek, 0, prog or 0)
        self.assertEqual([c[0] for c in dataFile.read.call_args_list], [(PCloudFile.blockSize,) for c in range(0, len(data) + 1)])

        for d in range(1, len(data) + 2):
            self.checkCall(mock_open, int(prog is not None) + d, 'test.txt.prog', 'wt')
        self.assertEqual([c[0] for c in progFile.write.call_args_list], [(str(min(maxProgress, (prog or 0) + c*PCloudFile.blockSize)),) for c in range(0, len(data) + 1)])

        self.assertEqual(len(mock_remove.call_args_list), 1)
        self.checkCall(mock_remove, 0, 'test.txt.prog')

    @unittest.mock.patch('pcloud.src.main.os.remove')
    @unittest.mock.patch('pcloud.src.main.os.path.isfile')
    @unittest.mock.patch('pcloud.src.main.open')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def __testError(self, fileIdOrPath, data, error, prog, mock_session, mock_request, mock_open, mock_isfile, mock_remove):
        # Setup mocks
        maxProgress = (prog or 0) + sum([len(d) for d in data])
        self.setupMock(mock_session, mock_request, 18, [{'result': 0, 'bytes': len(d)} for d in data] + [error])

        dataFile = unittest.mock.MagicMock()
        dataFile.__enter__.return_value = dataFile
        dataFile.read.side_effect = data + [b'ERROR123']

        progFile = unittest.mock.MagicMock()
        progFile.__enter__.return_value = progFile
        if prog is not None:
            progFile.read.side_effect = str(prog)

        unittest.mock.mock_open(mock_open)
        if prog is None:
            mock_open.side_effect = [dataFile] + [progFile]*(len(data) + 1)
        else:
            mock_open.side_effect = [progFile, dataFile] + [progFile]*(len(data) + 1)

        mock_isfile.return_value = prog is not None

        # Execute test
        PCloudFile.blockSize = 8
        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            expectedProgress = prog or 0
            with self.assertRaises(error if type(error) is type else PCloudError) as e:
                for p in pCloud.upload('test.txt', fileIdOrPath):
                    self.assertEqual(p, expectedProgress)
                    expectedProgress = min(expectedProgress + PCloudFile.blockSize, maxProgress)

            if type(error) is dict:
                self.assertEqual(e.exception.code, error['result'])
                self.assertEqual(str(e.exception), f"{error['error'][:-1]} ({error['result']})")

        # Check mocks
        for d in data:
            self.checkMock('PUT', 'https://pcloud.localhost/file_pwrite', params={'fd': 18}, data=d)
        self.checkMock('PUT', 'https://pcloud.localhost/file_pwrite', params={'fd': 18}, data=b'ERROR123')

        if prog is not None:
            self.checkCall(mock_open, 0, 'test.txt.prog', 'rt')
            self.assertEqual([c[0] for c in progFile.read.call_args_list], [()])

        self.checkCall(mock_open, int(prog is not None), 'test.txt', 'rb')
        self.checkCall(dataFile.seek, 0, prog or 0)
        self.assertEqual([c[0] for c in dataFile.read.call_args_list], [(PCloudFile.blockSize,) for c in range(0, len(data) + 1)])


        for d in range(1, len(data) + 2):
            self.checkCall(mock_open, int(prog is not None) + d, 'test.txt.prog', 'wt')
        self.assertEqual([c[0] for c in progFile.write.call_args_list], [(str(min(maxProgress, (prog or 0) + c*PCloudFile.blockSize)),) for c in range(0, len(data) + 1)])

        self.assertEqual(len(mock_remove.call_args_list), 0)

    def testIdOneChunkNoProgress(self):
        self.__testNormal(1, [b'01234567'], None)

    def testIdOneAndHalfChunksNoProgress(self):
        self.__testNormal(1, [b'01234567', b'89AB'], None)

    def testIdTwoChunksNoProgress(self):
        self.__testNormal(1, [b'01234567', b'89ABCDEF'], None)

    def testIdOneChunkProgress(self):
        self.__testNormal(1, [b'01234567'], 4)

    def testIdOneAndHalfChunksProgress(self):
        self.__testNormal(1, [b'01234567', b'89AB'], 4)

    def testIdTwoChunksProgress(self):
        self.__testNormal(1, [b'01234567', b'89ABCDEF'], 4)

    def testIdOneChunkProgress0(self):
        self.__testNormal(1, [b'01234567'], 0)

    def testIdOneAndHalfChunksProgress0(self):
        self.__testNormal(1, [b'01234567', b'89AB'], 0)

    def testIdTwoChunksProgress0(self):
        self.__testNormal(1, [b'01234567', b'89ABCDEF'], 0)

    def testPathOneChunkNoProgress(self):
        self.__testNormal('/New file', [b'01234567'], None)

    def testPathOneAndHalfChunksNoProgress(self):
        self.__testNormal('/New file', [b'01234567', b'89AB'], None)

    def testPathTwoChunksNoProgress(self):
        self.__testNormal('/New file', [b'01234567', b'89ABCDEF'], None)

    def testPathOneChunkProgress(self):
        self.__testNormal('/New file', [b'01234567'], 4)

    def testPathOneAndHalfChunksProgress(self):
        self.__testNormal('/New file', [b'01234567', b'89AB'], 4)

    def testPathTwoChunksProgress(self):
        self.__testNormal('/New file', [b'01234567', b'89ABCDEF'], 4)

    def testPathOneChunkProgress0(self):
        self.__testNormal('/New file', [b'01234567'], 0)

    def testPathOneAndHalfChunksProgress0(self):
        self.__testNormal('/New file', [b'01234567', b'89AB'], 0)

    def testPathTwoChunksProgress0(self):
        self.__testNormal('/New file', [b'01234567', b'89ABCDEF'], 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdNoChunksNoProgressError(self, result, error):
        self.__testError(1, [], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdOneChunkNoProgressError(self, result, error):
        self.__testError(1, [b'01234567'], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdOneAndHalfChunksNoProgressError(self, result, error):
        self.__testError(1, [b'01234567', b'89AB'], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdTwoChunksNoProgressError(self, result, error):
        self.__testError(1, [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdNoChunksProgressError(self, result, error):
        self.__testError(1, [], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdOneChunkProgressError(self, result, error):
        self.__testError(1, [b'01234567'], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdOneAndHalfChunksProgressError(self, result, error):
        self.__testError(1, [b'01234567', b'89AB'], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdTwoChunksProgressError(self, result, error):
        self.__testError(1, [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdNoChunksProgress0Error(self, result, error):
        self.__testError(1, [], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdOneChunkProgress0Error(self, result, error):
        self.__testError(1, [b'01234567'], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdOneAndHalfChunksProgress0Error(self, result, error):
        self.__testError(1, [b'01234567', b'89AB'], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testIdTwoChunksProgress0Error(self, result, error):
        self.__testError(1, [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathNoChunksNoProgressError(self, result, error):
        self.__testError('/New file', [], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathOneChunkNoProgressError(self, result, error):
        self.__testError('/New file', [b'01234567'], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathOneAndHalfChunksNoProgressError(self, result, error):
        self.__testError('/New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathTwoChunksNoProgressError(self, result, error):
        self.__testError('/New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, None)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathNoChunksProgressError(self, result, error):
        self.__testError('/New file', [], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathOneChunkProgressError(self, result, error):
        self.__testError('/New file', [b'01234567'], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathOneAndHalfChunksProgressError(self, result, error):
        self.__testError('/New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathTwoChunksProgressError(self, result, error):
        self.__testError('/New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 4)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathNoChunksProgress0Error(self, result, error):
        self.__testError('/New file', [], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathOneChunkProgress0Error(self, result, error):
        self.__testError('/New file', [b'01234567'], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathOneAndHalfChunksProgress0Error(self, result, error):
        self.__testError('/New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 0)

    @testdata.TestData([
        {'result': 1000, 'error': "Log in required."                                                     },
        {'result': 1007, 'error': "Invalid or closed file descriptor."                                   },
        {'result': 1009, 'error': "Please provide 'offset'."                                             },
        {'result': 2000, 'error': "Log in failed."                                                       },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 4000, 'error': "Too many login tries from this IP address."                           },
        {'result': 5003, 'error': "Write error, try reopening the file."                                 },
    ])
    def testPathTwoChunksProgress0Error(self, result, error):
        self.__testError('/New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 0)

    def testIdNoChunksNoProgressHttpError(self):
        self.__testError(1, [], requests.exceptions.HTTPError, None)

    def testIdOneChunkNoProgressHttpError(self):
        self.__testError(1, [b'01234567'], requests.exceptions.HTTPError, None)

    def testIdOneAndHalfChunksNoProgressHttpError(self):
        self.__testError(1, [b'01234567', b'89AB'], requests.exceptions.HTTPError, None)

    def testIdTwoChunksNoProgressHttpError(self):
        self.__testError(1, [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, None)

    def testIdNoChunksProgressHttpError(self):
        self.__testError(1, [], requests.exceptions.HTTPError, 4)

    def testIdOneChunkProgressHttpError(self):
        self.__testError(1, [b'01234567'], requests.exceptions.HTTPError, 4)

    def testIdOneAndHalfChunksProgressHttpError(self):
        self.__testError(1, [b'01234567', b'89AB'], requests.exceptions.HTTPError, 4)

    def testIdTwoChunksProgressHttpError(self):
        self.__testError(1, [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 4)

    def testIdNoChunksProgress0HttpError(self):
        self.__testError(1, [], requests.exceptions.HTTPError, 0)

    def testIdOneChunkProgress0HttpError(self):
        self.__testError(1, [b'01234567'], requests.exceptions.HTTPError, 0)

    def testIdOneAndHalfChunksProgress0HttpError(self):
        self.__testError(1, [b'01234567', b'89AB'], requests.exceptions.HTTPError, 0)

    def testIdTwoChunksProgress0HttpError(self):
        self.__testError(1, [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 0)

    def testPathNoChunksNoProgressHttpError(self):
        self.__testError('/New file', [], requests.exceptions.HTTPError, None)

    def testPathOneChunkNoProgressHttpError(self):
        self.__testError('/New file', [b'01234567'], requests.exceptions.HTTPError, None)

    def testPathOneAndHalfChunksNoProgressHttpError(self):
        self.__testError('/New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, None)

    def testPathTwoChunksNoProgressHttpError(self):
        self.__testError('/New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, None)

    def testPathNoChunksProgressHttpError(self):
        self.__testError('/New file', [], requests.exceptions.HTTPError, 4)

    def testPathOneChunkProgressHttpError(self):
        self.__testError('/New file', [b'01234567'], requests.exceptions.HTTPError, 4)

    def testPathOneAndHalfChunksProgressHttpError(self):
        self.__testError('/New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 4)

    def testPathTwoChunksProgressHttpError(self):
        self.__testError('/New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 4)

    def testPathNoChunksProgress0HttpError(self):
        self.__testError('/New file', [], requests.exceptions.HTTPError, 0)

    def testPathOneChunkProgress0HttpError(self):
        self.__testError('/New file', [b'01234567'], requests.exceptions.HTTPError, 0)

    def testPathOneAndHalfChunksProgress0HttpError(self):
        self.__testError('/New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 0)

    def testPathTwoChunksProgress0HttpError(self):
        self.__testError('/New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 0)
