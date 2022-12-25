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

class PCloudInfoMeta(type):
    """
    This metaclass allows to select the right :class:`PCloudInfo` subClass
    depending on the metadata.

    :param pc: :class:`~pcloud.PCloud` instance
    :param metadata: A dictionary containing folder or file information returned by *PCloud* API methods.
    """
    def __call__(cls, pc, metadata):
        for subClass in cls.__subclasses__():
            try:
                subClassId = subClass.classId
            except AttributeError: #pragma: no cover
                continue
            if subClassId in metadata:
                return subClass.__call__(pc, metadata)

        return super().__call__(pc, metadata)


class PCloudInfo(metaclass=PCloudInfoMeta):
    """
    Base class to represent *PCloud* folder of file information. The instances of this class will have the following attributes:
      - ``category`` An integer representing the item category
      - ``contentType`` A sirng containing the item MIME type
      - ``comments`` A string containing user comments associated to item
      - ``created`` A string representing item creation date (using the format )
      - ``hash`` An integer hash for the item
      - ``icon`` A string containing the item icon
      - ``id`` An integer representing the item id
      - ``isFolder`` A boolean value indicating whether the item is a folder
      - ``isMine`` A boolean value indicating whether the item belongs to the current user.
      - ``isShared`` A boolean value indicating whether the item is shared
      - ``modified`` A string representing item modification date (using the format )
      - ``name`` A string containing the item name
      - ``parentFolderId`` An integer representing the id of the parent folder
      - ``path`` A string containing the path to the item
      - ``size`` An integer representing the size of the file in bytes
      - ``hasThumb`` A boolean value indicating whether the item has been marked as favorite

    The instances of this class can be iterated through to get the contents of the item.
    Lazy-loading is implemented if the metadata has not been obtained with :meth:`PCloud.listFolder() <pcloud.PCloud.listFolder()>`
    with recursion enabled.

    :param pc: :class:`~pcloud.PCloud` instance
    :param metadata: A dictionary containing folder or file information returned by *PCloud* API methods.
    """

    def __init__(self, pCloud, metadata):
        self._pCloud = pCloud
        try:
            self.id = metadata[self.__class__.classId]
        except AttributeError: #pragma: no cover
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
    """
    Class representing *PCloud* file information. See :class:`PCloudInfo` for details.
    """

    classId = 'fileid'
    """ Metadata identifier supported by this classs """

    @property
    def isFolder(self):
        return False


class PCloudFolderInfo(PCloudInfo):
    """
    Class representing *PCloud* folder information. See :class:`PCloudInfo` for details.
    """

    classId = 'folderid'
    """ Metadata identifier supported by this classs """

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
