from .testfolder import PCloudTestFolder

class PCloudTestRootFolder(PCloudTestFolder):
    def __init__(self, contents=[], **kwArgs):
        super().__init__('', contents, 0, **kwArgs)
        del self._data['comments']

        self._data['path'] = '/'
        for child in self._contents:
            child._updatePath('/', 0)
