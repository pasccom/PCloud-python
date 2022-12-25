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

class PCloudTestObject:
    def __init__(self, **kwArgs):
        self._depth = None
        self._base = None
        self._includeFiles = True

        for k, v in kwArgs.items():
            if k in self._data:
                self._data[k] = v

    def _updatePath(self, parentPath, parentFolderId):
        self._data['parentfolderid'] = parentFolderId
        self._data['path'] = parentPath + self._data['name']

    def __iter__(self):
        if (self._base is None):
            for k, v in self._data.items():
                yield k, v

    def __call__(self, depth=None, base=None, files=True):
        self._depth = depth
        self._base = base
        self._includeFiles = files
        return self
