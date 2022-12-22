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
