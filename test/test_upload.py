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
    def __testFileNormal(self, fileIdOrPath, data, prog, mock_session, mock_request, mock_open, mock_isfile, mock_remove):
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
    def __testFolderNormal(self, folderIdOrPath, fileName, data, prog, mock_session, mock_request, mock_open, mock_isfile, mock_remove):
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
            for p in pCloud.upload('test.txt', folderIdOrPath, fileName):
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
    def __testFileError(self, fileIdOrPath, data, error, prog, mock_session, mock_request, mock_open, mock_isfile, mock_remove):
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

    @unittest.mock.patch('pcloud.src.main.os.remove')
    @unittest.mock.patch('pcloud.src.main.os.path.isfile')
    @unittest.mock.patch('pcloud.src.main.open')
    @unittest.mock.patch('pcloud.src.main.requests.request')
    @unittest.mock.patch('pcloud.src.main.requests.Session')
    def __testFolderError(self, folderIdOrPath, fileName, data, error, prog, mock_session, mock_request, mock_open, mock_isfile, mock_remove):
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
                for p in pCloud.upload('test.txt', folderIdOrPath, fileName):
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

    def testFileIdOneChunkNoProgress(self):
        self.__testFileNormal(1, [b'01234567'], None)

    def testFileIdOneAndHalfChunksNoProgress(self):
        self.__testFileNormal(1, [b'01234567', b'89AB'], None)

    def testFileIdTwoChunksNoProgress(self):
        self.__testFileNormal(1, [b'01234567', b'89ABCDEF'], None)

    def testFileIdOneChunkProgress(self):
        self.__testFileNormal(1, [b'01234567'], 4)

    def testFileIdOneAndHalfChunksProgress(self):
        self.__testFileNormal(1, [b'01234567', b'89AB'], 4)

    def testFileIdTwoChunksProgress(self):
        self.__testFileNormal(1, [b'01234567', b'89ABCDEF'], 4)

    def testFileIdOneChunkProgress0(self):
        self.__testFileNormal(1, [b'01234567'], 0)

    def testFileIdOneAndHalfChunksProgress0(self):
        self.__testFileNormal(1, [b'01234567', b'89AB'], 0)

    def testFileIdTwoChunksProgress0(self):
        self.__testFileNormal(1, [b'01234567', b'89ABCDEF'], 0)

    def testFilePathOneChunkNoProgress(self):
        self.__testFileNormal('/New file', [b'01234567'], None)

    def testFilePathOneAndHalfChunksNoProgress(self):
        self.__testFileNormal('/New file', [b'01234567', b'89AB'], None)

    def testFilePathTwoChunksNoProgress(self):
        self.__testFileNormal('/New file', [b'01234567', b'89ABCDEF'], None)

    def testFilePathOneChunkProgress(self):
        self.__testFileNormal('/New file', [b'01234567'], 4)

    def testFilePathOneAndHalfChunksProgress(self):
        self.__testFileNormal('/New file', [b'01234567', b'89AB'], 4)

    def testFilePathTwoChunksProgress(self):
        self.__testFileNormal('/New file', [b'01234567', b'89ABCDEF'], 4)

    def testFilePathOneChunkProgress0(self):
        self.__testFileNormal('/New file', [b'01234567'], 0)

    def testFilePathOneAndHalfChunksProgress0(self):
        self.__testFileNormal('/New file', [b'01234567', b'89AB'], 0)

    def testFilePathTwoChunksProgress0(self):
        self.__testFileNormal('/New file', [b'01234567', b'89ABCDEF'], 0)

    def testFolderIdOneChunkNoProgress(self):
        self.__testFolderNormal(0, 'New file', [b'01234567'], None)

    def testFolderIdOneAndHalfChunksNoProgress(self):
        self.__testFolderNormal(0, 'New file', [b'01234567', b'89AB'], None)

    def testFolderIdTwoChunksNoProgress(self):
        self.__testFolderNormal(0, 'New file', [b'01234567', b'89ABCDEF'], None)

    def testFolderIdOneChunkProgress(self):
        self.__testFolderNormal(0, 'New file', [b'01234567'], 4)

    def testFolderIdOneAndHalfChunksProgress(self):
        self.__testFolderNormal(0, 'New file', [b'01234567', b'89AB'], 4)

    def testFolderIdTwoChunksProgress(self):
        self.__testFolderNormal(0, 'New file', [b'01234567', b'89ABCDEF'], 4)

    def testFolderIdOneChunkProgress0(self):
        self.__testFolderNormal(0, 'New file', [b'01234567'], 0)

    def testFolderIdOneAndHalfChunksProgress0(self):
        self.__testFolderNormal(0, 'New file', [b'01234567', b'89AB'], 0)

    def testFolderIdTwoChunksProgress0(self):
        self.__testFolderNormal(0, 'New file', [b'01234567', b'89ABCDEF'], 0)

    def testFolderPathOneChunkNoProgress(self):
        self.__testFolderNormal('', 'New file', [b'01234567'], None)

    def testFolderPathOneAndHalfChunksNoProgress(self):
        self.__testFolderNormal('', 'New file', [b'01234567', b'89AB'], None)

    def testFolderPathTwoChunksNoProgress(self):
        self.__testFolderNormal('', 'New file', [b'01234567', b'89ABCDEF'], None)

    def testFolderPathOneChunkProgress(self):
        self.__testFolderNormal('', 'New file', [b'01234567'], 4)

    def testFolderPathOneAndHalfChunksProgress(self):
        self.__testFolderNormal('', 'New file', [b'01234567', b'89AB'], 4)

    def testFolderPathTwoChunksProgress(self):
        self.__testFolderNormal('', 'New file', [b'01234567', b'89ABCDEF'], 4)

    def testFolderPathOneChunkProgress0(self):
        self.__testFolderNormal('', 'New file', [b'01234567'], 0)

    def testFolderPathOneAndHalfChunksProgress0(self):
        self.__testFolderNormal('', 'New file', [b'01234567', b'89AB'], 0)

    def testFolderPathTwoChunksProgress0(self):
        self.__testFolderNormal('', 'New file', [b'01234567', b'89ABCDEF'], 0)

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
    def testFileIdNoChunksNoProgressError(self, result, error):
        self.__testFileError(1, [], {'result': result, 'error': error}, None)

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
    def testFileIdOneChunkNoProgressError(self, result, error):
        self.__testFileError(1, [b'01234567'], {'result': result, 'error': error}, None)

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
    def testFileIdOneAndHalfChunksNoProgressError(self, result, error):
        self.__testFileError(1, [b'01234567', b'89AB'], {'result': result, 'error': error}, None)

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
    def testFileIdTwoChunksNoProgressError(self, result, error):
        self.__testFileError(1, [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, None)

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
    def testFileIdNoChunksProgressError(self, result, error):
        self.__testFileError(1, [], {'result': result, 'error': error}, 4)

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
    def testFileIdOneChunkProgressError(self, result, error):
        self.__testFileError(1, [b'01234567'], {'result': result, 'error': error}, 4)

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
    def testFileIdOneAndHalfChunksProgressError(self, result, error):
        self.__testFileError(1, [b'01234567', b'89AB'], {'result': result, 'error': error}, 4)

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
    def testFileIdTwoChunksProgressError(self, result, error):
        self.__testFileError(1, [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 4)

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
    def testFileIdNoChunksProgress0Error(self, result, error):
        self.__testFileError(1, [], {'result': result, 'error': error}, 0)

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
    def testFileIdOneChunkProgress0Error(self, result, error):
        self.__testFileError(1, [b'01234567'], {'result': result, 'error': error}, 0)

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
    def testFileIdOneAndHalfChunksProgress0Error(self, result, error):
        self.__testFileError(1, [b'01234567', b'89AB'], {'result': result, 'error': error}, 0)

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
    def testFileIdTwoChunksProgress0Error(self, result, error):
        self.__testFileError(1, [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 0)

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
    def testFilePathNoChunksNoProgressError(self, result, error):
        self.__testFileError('/New file', [], {'result': result, 'error': error}, None)

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
    def testFilePathOneChunkNoProgressError(self, result, error):
        self.__testFileError('/New file', [b'01234567'], {'result': result, 'error': error}, None)

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
    def testFilePathOneAndHalfChunksNoProgressError(self, result, error):
        self.__testFileError('/New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, None)

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
    def testFilePathTwoChunksNoProgressError(self, result, error):
        self.__testFileError('/New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, None)

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
    def testFilePathNoChunksProgressError(self, result, error):
        self.__testFileError('/New file', [], {'result': result, 'error': error}, 4)

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
    def testFilePathOneChunkProgressError(self, result, error):
        self.__testFileError('/New file', [b'01234567'], {'result': result, 'error': error}, 4)

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
    def testFilePathOneAndHalfChunksProgressError(self, result, error):
        self.__testFileError('/New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 4)

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
    def testFilePathTwoChunksProgressError(self, result, error):
        self.__testFileError('/New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 4)

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
    def testFilePathNoChunksProgress0Error(self, result, error):
        self.__testFileError('/New file', [], {'result': result, 'error': error}, 0)

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
    def testFilePathOneChunkProgress0Error(self, result, error):
        self.__testFileError('/New file', [b'01234567'], {'result': result, 'error': error}, 0)

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
    def testFilePathOneAndHalfChunksProgress0Error(self, result, error):
        self.__testFileError('/New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 0)

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
    def testFilePathTwoChunksProgress0Error(self, result, error):
        self.__testFileError('/New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 0)

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
    def testFolderIdNoChunksNoProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [], {'result': result, 'error': error}, None)

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
    def testFolderIdOneChunkNoProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567'], {'result': result, 'error': error}, None)

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
    def testFolderIdOneAndHalfChunksNoProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, None)

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
    def testFolderIdTwoChunksNoProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, None)

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
    def testFolderIdNoChunksProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [], {'result': result, 'error': error}, 4)

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
    def testFolderIdOneChunkProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567'], {'result': result, 'error': error}, 4)

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
    def testFolderIdOneAndHalfChunksProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 4)

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
    def testFolderIdTwoChunksProgressError(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 4)

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
    def testFolderIdNoChunksProgress0Error(self, result, error):
        self.__testFolderError(0, 'New file', [], {'result': result, 'error': error}, 0)

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
    def testFolderIdOneChunkProgress0Error(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567'], {'result': result, 'error': error}, 0)

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
    def testFolderIdOneAndHalfChunksProgress0Error(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 0)

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
    def testFolderIdTwoChunksProgress0Error(self, result, error):
        self.__testFolderError(0, 'New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 0)

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
    def testFolderPathNoChunksNoProgressError(self, result, error):
        self.__testFolderError('', 'New file', [], {'result': result, 'error': error}, None)

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
    def testFolderPathOneChunkNoProgressError(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567'], {'result': result, 'error': error}, None)

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
    def testFolderPathOneAndHalfChunksNoProgressError(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, None)

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
    def testFolderPathTwoChunksNoProgressError(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, None)

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
    def testFolderPathNoChunksProgressError(self, result, error):
        self.__testFolderError('', 'New file', [], {'result': result, 'error': error}, 4)

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
    def testFolderPathOneChunkProgressError(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567'], {'result': result, 'error': error}, 4)

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
    def testFolderPathOneAndHalfChunksProgressError(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 4)

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
    def testFolderPathTwoChunksProgressError(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 4)

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
    def testFolderPathNoChunksProgress0Error(self, result, error):
        self.__testFolderError('', 'New file', [], {'result': result, 'error': error}, 0)

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
    def testFolderPathOneChunkProgress0Error(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567'], {'result': result, 'error': error}, 0)

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
    def testFolderPathOneAndHalfChunksProgress0Error(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567', b'89AB'], {'result': result, 'error': error}, 0)

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
    def testFolderPathTwoChunksProgress0Error(self, result, error):
        self.__testFolderError('', 'New file', [b'01234567', b'89ABCDEF'], {'result': result, 'error': error}, 0)

    def testFileIdNoChunksNoProgressHttpError(self):
        self.__testFileError(1, [], requests.exceptions.HTTPError, None)

    def testFileIdOneChunkNoProgressHttpError(self):
        self.__testFileError(1, [b'01234567'], requests.exceptions.HTTPError, None)

    def testFileIdOneAndHalfChunksNoProgressHttpError(self):
        self.__testFileError(1, [b'01234567', b'89AB'], requests.exceptions.HTTPError, None)

    def testFileIdTwoChunksNoProgressHttpError(self):
        self.__testFileError(1, [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, None)

    def testFileIdNoChunksProgressHttpError(self):
        self.__testFileError(1, [], requests.exceptions.HTTPError, 4)

    def testFileIdOneChunkProgressHttpError(self):
        self.__testFileError(1, [b'01234567'], requests.exceptions.HTTPError, 4)

    def testFileIdOneAndHalfChunksProgressHttpError(self):
        self.__testFileError(1, [b'01234567', b'89AB'], requests.exceptions.HTTPError, 4)

    def testFileIdTwoChunksProgressHttpError(self):
        self.__testFileError(1, [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 4)

    def testFileIdNoChunksProgress0HttpError(self):
        self.__testFileError(1, [], requests.exceptions.HTTPError, 0)

    def testFileIdOneChunkProgress0HttpError(self):
        self.__testFileError(1, [b'01234567'], requests.exceptions.HTTPError, 0)

    def testFileIdOneAndHalfChunksProgress0HttpError(self):
        self.__testFileError(1, [b'01234567', b'89AB'], requests.exceptions.HTTPError, 0)

    def testFileIdTwoChunksProgress0HttpError(self):
        self.__testFileError(1, [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 0)

    def testFilePathNoChunksNoProgressHttpError(self):
        self.__testFileError('/New file', [], requests.exceptions.HTTPError, None)

    def testFilePathOneChunkNoProgressHttpError(self):
        self.__testFileError('/New file', [b'01234567'], requests.exceptions.HTTPError, None)

    def testFilePathOneAndHalfChunksNoProgressHttpError(self):
        self.__testFileError('/New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, None)

    def testFilePathTwoChunksNoProgressHttpError(self):
        self.__testFileError('/New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, None)

    def testFilePathNoChunksProgressHttpError(self):
        self.__testFileError('/New file', [], requests.exceptions.HTTPError, 4)

    def testFilePathOneChunkProgressHttpError(self):
        self.__testFileError('/New file', [b'01234567'], requests.exceptions.HTTPError, 4)

    def testFilePathOneAndHalfChunksProgressHttpError(self):
        self.__testFileError('/New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 4)

    def testFilePathTwoChunksProgressHttpError(self):
        self.__testFileError('/New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 4)

    def testFilePathNoChunksProgress0HttpError(self):
        self.__testFileError('/New file', [], requests.exceptions.HTTPError, 0)

    def testFilePathOneChunkProgress0HttpError(self):
        self.__testFileError('/New file', [b'01234567'], requests.exceptions.HTTPError, 0)

    def testFilePathOneAndHalfChunksProgress0HttpError(self):
        self.__testFileError('/New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 0)

    def testFilePathTwoChunksProgress0HttpError(self):
        self.__testFileError('/New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 0)

    def testFolderIdNoChunksNoProgressHttpError(self):
        self.__testFolderError(0, 'New file', [], requests.exceptions.HTTPError, None)

    def testFolderIdOneChunkNoProgressHttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567'], requests.exceptions.HTTPError, None)

    def testFolderIdOneAndHalfChunksNoProgressHttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, None)

    def testFolderIdTwoChunksNoProgressHttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, None)

    def testFolderIdNoChunksProgressHttpError(self):
        self.__testFolderError(0, 'New file', [], requests.exceptions.HTTPError, 4)

    def testFolderIdOneChunkProgressHttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567'], requests.exceptions.HTTPError, 4)

    def testFolderIdOneAndHalfChunksProgressHttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 4)

    def testFolderIdTwoChunksProgressHttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 4)

    def testFolderIdNoChunksProgress0HttpError(self):
        self.__testFolderError(0, 'New file', [], requests.exceptions.HTTPError, 0)

    def testFolderIdOneChunkProgress0HttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567'], requests.exceptions.HTTPError, 0)

    def testFolderIdOneAndHalfChunksProgress0HttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 0)

    def testFolderIdTwoChunksProgress0HttpError(self):
        self.__testFolderError(0, 'New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 0)

    def testFolderPathNoChunksNoProgressHttpError(self):
        self.__testFolderError('', 'New file', [], requests.exceptions.HTTPError, None)

    def testFolderPathOneChunkNoProgressHttpError(self):
        self.__testFolderError('', 'New file', [b'01234567'], requests.exceptions.HTTPError, None)

    def testFolderPathOneAndHalfChunksNoProgressHttpError(self):
        self.__testFolderError('', 'New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, None)

    def testFolderPathTwoChunksNoProgressHttpError(self):
        self.__testFolderError('', 'New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, None)

    def testFolderPathNoChunksProgressHttpError(self):
        self.__testFolderError('', 'New file', [], requests.exceptions.HTTPError, 4)

    def testFolderPathOneChunkProgressHttpError(self):
        self.__testFolderError('', 'New file', [b'01234567'], requests.exceptions.HTTPError, 4)

    def testFolderPathOneAndHalfChunksProgressHttpError(self):
        self.__testFolderError('', 'New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 4)

    def testFolderPathTwoChunksProgressHttpError(self):
        self.__testFolderError('', 'New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 4)

    def testFolderPathNoChunksProgress0HttpError(self):
        self.__testFolderError('', 'New file', [], requests.exceptions.HTTPError, 0)

    def testFolderPathOneChunkProgress0HttpError(self):
        self.__testFolderError('', 'New file', [b'01234567'], requests.exceptions.HTTPError, 0)

    def testFolderPathOneAndHalfChunksProgress0HttpError(self):
        self.__testFolderError('', 'New file', [b'01234567', b'89AB'], requests.exceptions.HTTPError, 0)

    def testFolderPathTwoChunksProgress0HttpError(self):
        self.__testFolderError('', 'New file', [b'01234567', b'89ABCDEF'], requests.exceptions.HTTPError, 0)
