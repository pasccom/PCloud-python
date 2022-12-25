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

from pcloud import PCloud
from pcloud.src.error import PCloudError

from PythonUtils import testdata

class TestUserInfo(AuthTestCase):
    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testNormal(self, mock_request):
        self.setupMockNormal(mock_request, {
            'result': 0,
            'userid': 123456,
            'email': 'perso@localhost',
            'language': 'fr',
            'currency': 'EUR',
            'quota': 2199023255552,
            'usedquota': 123456789,
            'publiclinkquota': 2199023255552,
            'trashrevretentiondays': 30,
            'registered': 'Sun, 02 Feb 2020 20:20:20 +0000',
            'premiumexpires': 'Fri, 01 Jan 2100 06:08:08 +0000',
            'plan': 0,
            'emailverified': True,
            'agreedwithpp': True,
            'haspassword': True,
            'business': False,
            'premium': True,
            'premiumlifetime': True,
            'usedpublinkbranding': False,
            'haspaidrelocation': False,
            'cryptosetup': False,
            'cryptosubscription': False,
            'cryptolifetime': False,
            'journey': {
                'steps': {
                    'verifymail': True,
                    'uploadfile': True,
                    'autoupload': False,
                    'downloadapp': False,
                    'downloaddrive': False,
                    'sentinvitation': False
                }
            }
        })

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            info = pCloud.userInfo()

        self.checkMock('GET', 'https://pcloud.localhost/userinfo')
        self.assertEqual(info['userid'], 123456)
        self.assertEqual(info['email'], 'perso@localhost')
        self.assertEqual(info['language'], 'fr')
        self.assertEqual(info['currency'], 'EUR')
        self.assertEqual(info['quota'], 2199023255552)
        self.assertEqual(info['usedquota'], 123456789)
        self.assertEqual(info['publiclinkquota'], 2199023255552)
        self.assertEqual(info['trashrevretentiondays'], 30)
        self.assertEqual(info['registered'], 'Sun, 02 Feb 2020 20:20:20 +0000')
        self.assertEqual(info['premiumexpires'], 'Fri, 01 Jan 2100 06:08:08 +0000')
        self.assertEqual(info['plan'], 0)
        self.assertEqual(info['emailverified'], True)
        self.assertEqual(info['agreedwithpp'], True)
        self.assertEqual(info['haspassword'], True)
        self.assertEqual(info['business'], False)
        self.assertEqual(info['premium'], True)
        self.assertEqual(info['premiumlifetime'], True)
        self.assertEqual(info['usedpublinkbranding'], False)
        self.assertEqual(info['haspaidrelocation'], False)
        self.assertEqual(info['cryptosetup'], False)
        self.assertEqual(info['cryptosubscription'], False)
        self.assertEqual(info['cryptolifetime'], False)


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
                info = pCloud.userInfo()

            self.assertEqual(e.exception.code, result)
            self.assertEqual(str(e.exception), f"{error[:-1]} ({result})")

        self.checkMock('GET', 'https://pcloud.localhost/userinfo')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testHttpError(self, mock_request):
        self.setupMockHttpError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.HTTPError) as e:
                info = pCloud.userInfo()

        self.checkMock('GET', 'https://pcloud.localhost/userinfo')

    @unittest.mock.patch('pcloud.src.main.requests.request')
    def testConnectionError(self, mock_request):
        self.setupMockConnectionError(mock_request)

        with PCloud('https://pcloud.localhost/') as pCloud:
            pCloud.username = 'username'
            pCloud.password = 'password'

            with self.assertRaises(requests.exceptions.ConnectionError) as e:
                info = pCloud.userInfo()

        self.checkMock('GET', 'https://pcloud.localhost/userinfo')
