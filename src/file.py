from warnings import warn as warning

from .error import PCloudError

class PCloudFile:
    blockSize = 524288

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
        return self.__pCloud.readFile(self.__fd, count, offset=offset)

    def write(self, data, offset=None):
        return self.__pCloud.writeFile(self.__fd, data, offset=offset)

    def truncate(self, length):
        self.__pCloud.truncateFile(self.__fd, length)

    def seek(self, offset, origin=0):
        return self.__pCloud.seekFile(self.__fd, offset, origin)

    def uploadFile(self, srcFile, offset):
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
        return self.__pCloud.sizeFile(self.__fd)

    @property
    def offset(self):
        return self.__pCloud.offsetFile(self.__fd)

    @offset.setter
    def offset(self, offset):
        self.__pCloud.seekFile(self.__fd, offset)

    def close(self):
        self.__pCloud.closeFile(self.__fd)
        self.__isOpen = False
