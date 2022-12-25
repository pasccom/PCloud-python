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

import random

from .testobject import PCloudTestObject

class PCloudTestFile(PCloudTestObject):
    def __init__(self, name, fildId=random.randint(1, 4294967296), **kwArgs):
        self._data = {
            #'path': '/' + name
            'name'       :  name,
            'fileid'     : fildId,
            'isfolder'   : False,
            'id'         : 'f' + str(fildId),
            #'parentfolderid': 0,
            'icon'       : 'document',
            'created'    : 'Sun, 2 Feb 2020 20:20:20 +0000',
            'modified'   : 'Sun, 2 Feb 2020 20:20:20 +0000',
            'ismine'     : True,
            'thumb'      : False,
            'isshared'   : False,
            'comments'   : 0,
            'category'   : 4,
            'hash'       : 1234567890123456789,
            'size'       : 123456,
            'contenttype': 'application/pdf',
            'icon'       : 'document',
        }
        super().__init__(**kwArgs)

    def __iter__(self):
        if (self._base is None) or (self._base == self._data['path']) or (self._base == self._data['fileid']):
            for k, v in self._data.items():
                yield k, v

    def check(self, testSelf, r):
        attrMap = {
            'category'      : 'category',
            'contenttype'   : 'contentType',
            'comments'      : 'comments',
            'created'       : 'created',
            'hash'          : 'hash',
            'icon'          : 'icon',
            'isfolder'      : 'isFolder',
            'ismine'        : 'isMine',
            'isshared'      : 'isShared',
            'modified'      : 'modified',
            'name'          : 'name',
            'parentfolderid': 'parentFolderId',
            'path'          : 'path',
            'size'          : 'size',
            'thumb'         : 'hasThumb',
        }
        for k in self._data:
            if (self._base is None) or (self._base == self._data['path']) or (self._base == self._data['fileid']):
                if (k == 'fileid'):
                    continue
                if (k == 'id'):
                    testSelf.assertEqual(r.id, int(self._data[k][1:]))
                else:
                    testSelf.assertTrue(hasattr(r, attrMap[k]), f"{r} has no attribute {attrMap[k]}")
                    testSelf.assertEqual(getattr(r, attrMap[k]), self._data[k])
