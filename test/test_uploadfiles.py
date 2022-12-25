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

from .testcase_auth import AuthTestCase
from .objects import *

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestUploadFiles(AuthTestCase):
    file1 = 'file1'
    file2 = 'file2'
    progresId = 'progress'

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRoot0(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {})

        self.assertEqual(len(mock_request.call_args_list), 0)
        self.assertEqual(len(files), 0)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRoot1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file': self.__class__.file1})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRoot2(self, mock_request):
        roots = [PCloudTestRootFolder([PCloudTestFile('New file1', 1)]), PCloudTestRootFolder([PCloudTestFile('New file2', 2)])]
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(roots[0](base=1)), dict(roots[1](base=2))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file1': self.__class__.file1, 'New file2': self.__class__.file2})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0}, files={
            'New file1': ('New file1', self.__class__.file1),
            'New file2': ('New file2', self.__class__.file2),
        })
        self.assertEqual(len(files), 2)
        roots[0].check(self, files[0])
        roots[1].check(self, files[1])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdSubfolder0(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file', 2)], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=2))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(1, {})

        self.assertEqual(len(mock_request.call_args_list), 0)
        self.assertEqual(len(files), 0)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdSubfolder1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file', 2)], 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=2))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(1, {'New file': self.__class__.file1})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 1}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])


    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdSubfolder2(self, mock_request):
        roots = [PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file1', 2)], 1)]), PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file2', 3)], 1)])]
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(roots[0](base=2)), dict(roots[1](base=3))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(1, {'New file1': self.__class__.file1, 'New file2': self.__class__.file2})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 1}, files={
            'New file1': ('New file1', self.__class__.file1),
            'New file2': ('New file2', self.__class__.file2),
        })
        self.assertEqual(len(files), 2)
        roots[0].check(self, files[0])
        roots[1].check(self, files[1])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathRoot0(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base='/New file'))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles('/', {})

        self.assertEqual(len(mock_request.call_args_list), 0)
        self.assertEqual(len(files), 0)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathRoot1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file')])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base='/New file'))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles('/', {'New file': self.__class__.file1})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'path': '/'}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathRoot2(self, mock_request):
        roots = [PCloudTestRootFolder([PCloudTestFile('New file1')]), PCloudTestRootFolder([PCloudTestFile('New file2')])]
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(roots[0](base='/New file1')), dict(roots[1](base='/New file2'))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles('/', {'New file1': self.__class__.file1, 'New file2': self.__class__.file2})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'path': '/'}, files={
            'New file1': ('New file1', self.__class__.file1),
            'New file2': ('New file2', self.__class__.file2),
        })
        self.assertEqual(len(files), 2)
        roots[0].check(self, files[0])
        roots[1].check(self, files[1])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathSubfolder0(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file')])])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base='/Test/New file'))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles('/Test', {})

        self.assertEqual(len(mock_request.call_args_list), 0)
        self.assertEqual(len(files), 0)

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathSubfolder1(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file')])])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base='/Test/New file'))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles('/Test', {'New file': self.__class__.file1})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'path': '/Test'}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPathSubfolder2(self, mock_request):
        roots = [PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file1')])]), PCloudTestRootFolder([PCloudTestFolder('Test', [PCloudTestFile('New file2')])])]
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(roots[0](base='/Test/New file1')), dict(roots[1](base='/Test/New file2'))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles('/Test', {'New file1': self.__class__.file1, 'New file2': self.__class__.file2})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'path': '/Test'}, files={
            'New file1': ('New file1', self.__class__.file1),
            'New file2': ('New file2', self.__class__.file2),
        })
        self.assertEqual(len(files), 2)
        roots[0].check(self, files[0])
        roots[1].check(self, files[1])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRootProgressId(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file': self.__class__.file1}, progressId=self.__class__.progresId)

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0, 'progresshash': self.__class__.progresId}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRootNoOver(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file': self.__class__.file1}, overwrite=False)

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0, 'renameifexists': True}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRootOver(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file': self.__class__.file1}, overwrite=True)

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0, 'renameifexists': False}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRootNoPartial(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file': self.__class__.file1}, partial=False)

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0, 'nopartial': True}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testIdRootPartial(self, mock_request):
        root = PCloudTestRootFolder([PCloudTestFile('New file', 1)])
        self.setupMockNormal(mock_request, {'result': 0, 'metadata': [dict(root(base=1))]})

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            files = pCloud.uploadFiles(0, {'New file': self.__class__.file1}, partial=True)

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0, 'nopartial': False}, files={
            'New file': ('New file', self.__class__.file1),
        })
        self.assertEqual(len(files), 1)
        root.check(self, files[0])

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
                files = pCloud.uploadFiles(0, {'New file': self.__class__.file1})

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0}, files={
            'New file': ('New file', self.__class__.file1),
        })

    @testdata.TestData([
        {'result': 2001, 'error': "Invalid file/folder name."                                            },
        {'result': 2003, 'error': "Access denied, you do not have permissions to preform this operation."},
        {'result': 2005, 'error': "Directory does not exist."                                            },
        {'result': 2008, 'error': "User is over quota."                                                  },
        {'result': 2041, 'error': "Connection broken."                                                   },
        {'result': 5001, 'error': "Internal upload error."                                               },
    ])
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testPCloudError(self, mock_request, result, error):
        self.setupMockError(mock_request, result, error)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(PCloudError) as e:
                files = pCloud.uploadFiles(0, {'New file': self.__class__.file1})

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0}, files={
            'New file': ('New file', self.__class__.file1),
        })

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                files = pCloud.uploadFiles(0, {'New file': self.__class__.file1})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0}, files={
            'New file': ('New file', self.__class__.file1),
        })

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                files = pCloud.uploadFiles(0, {'New file': self.__class__.file1})

        self.checkMock('POST', 'https://pcloud.localhost/uploadfile', params={'folderid': 0}, files={
            'New file': ('New file', self.__class__.file1),
        })
