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

from .error import PCloudError

class PCloudResponse:
    def __init__(self, data):
        self.__data = data

    def __contains__(self, name):
        return (name != 'result') and (name in self.__data)

    def __getitem__(self, name):
        if (name == 'result'): #pragma: no cover
            raise KeyError("No such key: 'result'")
        return self.__data[name]

    def __delitem__(self, name):
        if (name == 'result'): #pragma: no cover
            raise KeyError("No such key: 'result'")
        del self.__data[name]

    def __repr__(self): #pragma: no cover
        r = "PCloudResponse(\n"
        for k, v in self.__data.items():
            if (k != 'result'):
                r += f"    {k}: {v!r}\n"
        r += ")"
        return r

    @property
    def result(self):
        return int(self.__data['result'])

    def raise_for_status(self):
        if (self.result != 0):
            raise PCloudError(self.result)
