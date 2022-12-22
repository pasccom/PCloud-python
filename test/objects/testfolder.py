import random

from .testobject import PCloudTestObject

class PCloudTestFolder(PCloudTestObject):
    def __init__(self, name, contents=[], folderId=random.randint(1, 4294967296), **kwArgs):
        self._data = {
            #'path': '/' + name,
            'name'    : name,
            'folderid': folderId,
            'isfolder': True,
            'id'      : 'd' + str(folderId),
            #'parentfolderid': 0,
            'icon'    : 'folder',
            'created' : 'Sun, 2 Feb 2020 20:20:20 +0000',
            'modified': 'Sun, 2 Feb 2020 20:20:20 +0000',
            'ismine'  : True,
            'thumb'   : False,
            'isshared': False,
            'comments': 0,
        }
        self._contents = contents
        super().__init__(**kwArgs)

    def _updatePath(self, parentPath, parentFolderId):
        super()._updatePath(parentPath, parentFolderId)

        for child in self._contents:
            child._updatePath(self._data['path'] + '/', self._data['folderid'])

    def __iter__(self):
        if (self._base is None) or ((type(self._base) is str) and (self._data['path'] == self._base)) or ((type(self._base) is int) and (self._data['folderid'] == self._base)):
            for k, v in self._data.items():
                yield k, v
            if self._includeFiles:
                if self._depth is None:
                    yield 'contents', [dict(child) for child in self._contents]
                elif (self._depth > 0):
                    yield 'contents', [dict(child(depth=self._depth - 1)) for child in self._contents]
            else:
                if self._depth is None:
                    yield 'contents', [dict(child(files=False)) for child in self._contents if type(child) is not PCloudTestFile]
                elif (self._depth > 0):
                    yield 'contents', [dict(child(depth=self._depth - 1, files=False)) for child in self._contents if type(child) is not PCloudTestFile]
        else:
            for child in self._contents:
                if (type(self._base) is str) and self._base.startswith(child._data['path']):
                    for kv in child(depth=self._depth, base=self._base, files=self._includeFiles):
                        yield kv
                    break
                if (type(self._base) is int):
                    for kv in child(depth=self._depth, base=self._base, files=self._includeFiles):
                        yield kv
            else:
                if (type(self._base) is str):
                    raise ValueError(f"base not found: {self._base}")

    def check(self, testSelf, r):
        attrMap = {
            'comments'      : 'comments',
            'created'       : 'created',
            'icon'          : 'icon',
            'isfolder'      : 'isFolder',
            'ismine'        : 'isMine',
            'isshared'      : 'isShared',
            'modified'      : 'modified',
            'name'          : 'name',
            'parentfolderid': 'parentFolderId',
            'path'          : 'path',
            'thumb'         : 'hasThumb',
        }
        if (self._base is None) or ((type(self._base) is str) and (self._data['path'] == self._base)) or ((type(self._base) is int) and (self._data['folderid'] == self._base)):
            for k in self._data:
                if (k == 'folderid'):
                    continue
                if (k == 'id'):
                    testSelf.assertEqual(r.id, int(self._data[k][1:]))
                else:
                    testSelf.assertTrue(hasattr(r, attrMap[k]), f"{r} has no attribute {attrMap[k]}")
                    testSelf.assertEqual(getattr(r, attrMap[k]), self._data[k])
            if (self._depth is None) or (self._depth > 0):
                testSelf.assertEqual(len(r), sum([self._includeFiles or (type(child) is PCloudTestFile) for child in self._contents]))
                for child, expectedChild in zip(r, [child for child in self._contents if self._includeFiles or (type(child) is PCloudTestFile)]):
                    expectedChild.check(testSelf, child)
        else:
            for child in self._contents:
                if (type(self._base) is str) and self._base.startswith(child._data['path']):
                    child.check(testSelf, r)
                    break
                if (type(self._base) is int):
                    child.check(testSelf, r)
            else:
                if (type(self._base) is str):
                    raise ValueError(f"base not found: {self._base}")
