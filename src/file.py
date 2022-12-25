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

from warnings import warn as warning

from .error import PCloudError

class PCloudFile:
    """
    Class representation for *PCloud* API file objects (a.k.a file descriptors).

    *PCloud* file objects are obtained and used as follows::

        with pCloud.openFile(1) as pCloudFile:
            print(pCloudFile.read(1024))


        with pCloud.createFile(0, 'test.txt') as pCloudFile:
            print(pCloudFile.write('Hello world!'))

    :param pCloud: :class:`~pcloud.PCloud` instance
    :param fd: An integer file descriptor.
    :param fileId: An integer file id.
    """

    blockSize = 524288
    """ Default size for the data blocks read by :meth:`downloadFile()` or written by :meth:`uploadFile()` """

    def __init__(self, pCloud, fd, fileId):
        self.__pCloud = pCloud
        self.__fd = fd
        self.__fileId = fileId
        self.__isOpen = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        attempts = 0
        while (self.__isOpen):
            attempts += 1
            try:
                self.close()
            except PCloudError as e:
                if (e.code == 1007):
                    break
                if (attempts >= 3):
                    warning(f"Could not close file {self.__fd} due to exception:\n {e.__class__.__name__ }: {e}")
                    break
            except BaseException as e:
                if (attempts >= 3):
                    warning(f"Could not close file {self.__fd} due to exception:\n {e.__class__.__name__ }: {e}")
                    break

    def read(self, count, offset=None):
        """
        Reads data at the current pointer position from the file.

        :param count: An integer giving the number of bytes to read.
        :param offset: An optional integer giving the position where to read data in the file.
        :return: A byte array containing the data that has been read in the file
        """
        return self.__pCloud.readFile(self.__fd, count, offset=offset)

    def write(self, data, offset=None):
        """
        Writes the given data to the file at the current pointer position.

        :param data: A byte array containing the data to be written in the file.
        :param offset: An optional integer giving the position where to write the data in the file.
        :return: A byte array containing the data that has been read in the file
        """
        return self.__pCloud.writeFile(self.__fd, data, offset=offset)

    def truncate(self, length):
        """
        Trunctate the file to the given length.

        :param length: An integer giving the length at which to truncate the file.
        """
        self.__pCloud.truncateFile(self.__fd, length)

    def seek(self, offset, origin=0):
        """
        Sets the position of the file pointer.

        :param offset: An integer giving the new position of the file pointer.
        :param origin: Optional :class:`PCloud.OffsetOrigin <pcloud.PCloud.OffsetOrigin>`.
        :return: An integer giving the new file pointer position (from the start of the file).
        """
        return self.__pCloud.seekFile(self.__fd, offset, origin)

    def uploadFile(self, srcFile, offset):
        """
        Uploads the given file the the *PCloud* file by blocks of size :attr:`~PCloudFile.blockSize`.

        .. note::
            This method is meant to be used internally by :meth:`PCloud.upload() <pcloud.PCloud.upload()>`

        :param srcFile: A ``file`` from wich to read data.
        :param offset: The offset at which to start reading data.
        :yield: The current file pointer position.
        """
        srcFile.seek(offset)
        yield offset

        while True:
            data = srcFile.read(self.__class__.blockSize)
            #print(f'data: "{data}"')
            if (len(data) == 0):
                return

            offset += self.write(data, offset)
            yield offset

    def downloadFile(self, destFile, offset):
        """
        Downloads the *PCloud* file to the given file by blocks of size :attr:`~PCloudFile.blockSize`.

        .. note::
            This method is meant to be used internally by :meth:`PCloud.download() <pcloud.PCloud.download()>`

        :param srcFile: A ``file`` to which to write data.
        :param offset: The offset at which to start writing data.
        :yield: The current file pointer position.
        """
        destFile.seek(offset)
        yield offset

        while True:
            data = self.read(self.__class__.blockSize, offset)
            #print(f'data: "{data}"')
            if (len(data) == 0):
                return

            destFile.write(data)
            offset += len(data)
            yield offset

    @property
    def size(self):
        """
        An integer representing the size of the file in bytes.
        """
        return self.__pCloud.sizeFile(self.__fd)

    @property
    def offset(self):
        """
        An integer representing the file pointer position (from the start of the file).
        """
        return self.__pCloud.offsetFile(self.__fd)

    @offset.setter
    def offset(self, offset):
        self.__pCloud.seekFile(self.__fd, offset)

    def close(self):
        """
        Closes the file.
        """
        self.__pCloud.closeFile(self.__fd)
        self.__isOpen = False
