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

import unittest
import warnings

class MetaTestCase(type):
    def __new__(cls, name, bases, attrs):
        for n, v in attrs.items():
            if n.startswith('test'):
                attrs[n] = cls.checkWarnings(v, n)
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def formatWarnings(warningMessages):
        return '  - ' + '\n  - '.join([f'{m.message} ({m.filename}:{m.lineno})' for m in warningMessages])

    @classmethod
    def checkWarnings(cls, fun, name):
        def wrapper(self, *args, **kwArgs):
            with warnings.catch_warnings(record=True) as w:
                fun(self, *args, **kwArgs)

                self.assertEqual(len(w), 0, f'Funcion {name} raised warnings:\n{cls.formatWarnings(w)}')
        return wrapper

class TestCase(unittest.TestCase, metaclass=MetaTestCase):
    def checkCall(self, mock, call, *args, **kwArgs):
        self.assertGreater(len(mock.call_args_list), call)
        self.assertEqual(len(mock.call_args_list[call]), 2)
        self.assertEqual(mock.call_args_list[call][0], args)
        for ak, av in kwArgs.items():
            self.assertIn(ak, mock.call_args_list[call][1])
            if (ak == 'params'):
                for pk, pv in av.items():
                    self.assertIn(pk, mock.call_args_list[call][1][ak])
                    self.assertEqual(mock.call_args_list[call][1][ak][pk], pv)
            else:
                self.assertEqual(mock.call_args_list[call][1][ak], av)
