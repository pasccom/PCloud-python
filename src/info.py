class PCloudInfoMeta(type):
    def __call__(cls, pc, metadata):
        for subClass in cls.__subclasses__():
            try:
                subClassId = subClass.classId
            except AttributeError:
                continue
            if subClassId in metadata:
                return subClass.__call__(pc, metadata)

        return super().__call__(pc, metadata)


class PCloudInfo(metaclass=PCloudInfoMeta):
    def __init__(self, pCloud, metadata):
        self._pCloud = pCloud
        try:
            self.id = metadata[self.__class__.classId]
        except AttributeError:
            self.id = None
        attrMap = {
            'category'      : 'category',
            'contenttype'   : 'contentType',
            'comments'      : 'comments',
            'created'       : 'created',
            'hash'          : 'hash',
            'icon'          : 'icon',
            'ismine'        : 'isMine',
            'isshared'      : 'isShared',
            'modified'      : 'modified',
            'name'          : 'name',
            'parentfolderid': 'parentFolderId',
            'path'          : 'path',
            'size'          : 'size',
            'thumb'         : 'hasThumb',
        }
        for k, v in attrMap.items():
            if k in metadata:
                setattr(self, v, metadata[k])

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def __len__(self):
        return 0

    def __iter__(self):
        return iter([])


class PCloudFileInfo(PCloudInfo):
    classId = 'fileid'

    @property
    def isFolder(self):
        return False


class PCloudFolderInfo(PCloudInfo):
    classId = 'folderid'

    def __init__(self, pCloud, metadata):
        super().__init__(pCloud, metadata)
        if 'contents' in metadata:
            self.__contents = [PCloudInfo(self._pCloud, o) for o in metadata['contents']]
        else:
            self.__contents = None

    def __fetchContents(self):
        self.__contents = self._pCloud.listFolder(self).__contents

    def __len__(self):
        if self.__contents is None:
            self.__fetchContents()
        return len(self.__contents)

    def __getitem__(self, index):
        if self.__contents is None:
            self.__fetchContents()
        return self.__contents[index]

    def __iter__(self):
        if self.__contents is None:
            self.__fetchContents()
        return iter(self.__contents)

    @property
    def isFolder(self):
        return True
