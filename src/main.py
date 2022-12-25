import os
import time
import requests

from warnings import warn as warning
from enum import Enum, IntFlag
from hashlib import sha1

from .error import PCloudError
from .response import PCloudResponse
from .info import PCloudInfo
from .file import PCloudFile

class PCloud:
    """
    This is the entry point of *PCloud* API implementation.

    Most of the methods of this class can raise exception related to network issues (e.g. ConnectionError),
    protocol issues (e.g. requests.exception.HttpError) or *PCloud* API error (:class:`~.error.PCloudError`).

    :param hostname: Optional user-provided URL to a *PCloud* server
    :param username: Optional user name
    :param password: Optional password

    .. note::
        User name and password must be available when using methods requiring authentication.

        They can either be provided to the constructor or later, before calling a method requiring authentication.

    It should be used as follows::

        with PCloud() as pCloud:
            pCloud.username = "username"
            pCloud.password = "password"

            pCloud.userInfo()
    """

    class HashAlgorithm(Enum):
        """
        Hashing algorithms implemented by *PCloud*

        To check the integrity of a file, getting the hash of a file is sufficient
        and much more effficient than downloading it.
        """
        def __new__(cls, value, length=None):
            obj = super(Enum, cls).__new__(cls)
            obj._value_ = value
            obj.length = length
            return obj

        SHA256 = ('sha256', 64)
        """
        SHA-256 Hashing algorithm (256-bit checksum represented as a string of 64 lowercase hexadecimal digits).

        :meta hide-value:
        """
        SHA1   = ('sha1',   40)
        """
        SHA-1 Hashing algorithm (160-bit checksum represented as a string of 40 lowercase hexadecimal digits).

        :meta hide-value:
        """
        MD5    = ('md5',    32)
        """
        MD-5 Hashing algorithm (128-bit checksum represented as a string of 32 lowercase hexadecimal digits).

        :meta hide-value:
        """
        ALL    = ('all',      )


    class FileOpenFlags(IntFlag):
        """
        File open flags (used when opening and creating files).
        """

        O_WRITE  = 0x0002
        """
        Make the file writable.

        :meta hide-value:
        """
        O_CREAT  = 0x0040
        """
        Force new file creation (fails if the file already exist).

        :meta hide-value:
        """
        O_EXCL   = 0x0080
        """
        Excusive usage (prevent the file to be used multiple times).

        :meta hide-value:
        """
        O_TRUNC  = 0x0200
        """
        Erase the contents of an existing file.

        :meta hide-value:
        """
        O_APPEND = 0x0400
        """
        Append content to en existing file (the file pointer is initialized at the end of the file).

        :meta hide-value:
        """


    class OffsetOrigin(Enum):
        """
        Offset reference (used when modifying file pointer).
        """

        Begin   = 0
        """
        The offset is absolute (from the start of the file).

        :meta hide-value:
        """
        Current = 1
        """
        The offset is relative (from the current file pointer).

        :meta hide-value:
        """
        End     = 2
        """
        The offset is counted from the end of the file.

        :meta hide-value:
        """

        def __int__(self):
            return self.value


    defaultServer = 'https://eapi.pcloud.com/'
    """ Default *PCloud* API server, which will be used if the user does not provide one and none can be obtained using :meth:`getApiServer()` """

    def __init__(self, hostname=None, username=None, password=None):
        self.__hostnames = [hostname, PCloud.defaultServer] if (hostname is not None) else []
        self.__authtoken = None
        self.username = username
        self.password = password

        self.__sessions = {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        attempts = 0
        while (attempts < 3):
            attempts += 1
            try:
                if self.logout():
                    print("Logged out")
                    break
            except BaseException as e:
                if (attempts >= 3):
                    warning(f"Could not logout due to exception:\n {e.__class__.__name__ }: {e}")
                    break
        else:
            warning("Could not logout")
        return False

    @property
    def authenticated(self):
        """
            Indicates whether the user is authenticated to the *PCloud* API.
        """
        return (self.__authtoken is not None)

    def currentServer(self):
        """
        Get information on the *PCloud* API server which is currently being used.

        :return: A dictionnary containing information on the *PCloud* API server.
        """
        return self.__sendNoAuthRequest('GET', 'currentserver')

    def getApiServer(self, binary=False):
        """
        Get the best API server URLs from *PClould* (depending on user location).
        :param binary: Whether to get a binary API server
        :return: A list of string containing the URLs to the best *PCloud* API servers

        .. note::
            This method is used internally so that the best *PCloud* API server is used.
        """
        r = self.__sendNoAuthRequest('GET', 'getapiserver')
        if binary:
            return ['https://' + host + '/' for host in r['binapi']]
        else:
            return ['https://' + host + '/' for host in r['api']]

    def getIp(self):
        """
        Get the user IP seen from the *PCloud* API server

        :return: A string representing the user IP.
        """
        r = self.__sendNoAuthRequest('GET', 'getip')
        return r['ip']

    def getDigest(self):
        """
        Get an authentication digest.

        .. note::
            This method is used internally to authenticate the user on the server.

        :return: A string containing the authentication digest.
        """
        r = self.__sendNoAuthRequest('GET', 'getdigest')
        return r['digest']

    def userInfo(self):
        """
        Get user information

        .. note::
            This method requires the user to be authenticated.

        :return: A dictionnary containing information of the currently autenticated user.
        """
        return self.__sendAuthRequest('GET', 'userinfo')

    def logout(self):
        """
        Log the user out.

        .. note::
            This method requires the user to be authenticated.

        :return: A boolean value indicating whether the user was actually logged out.
        """

        if self.__authtoken is None:
            return True
        try:
            r = self.__sendAuthRequest('GET', 'logout')
        except PCloudError as e:
            if e.code in [1000, 2000, 4000]:
                return True
            raise e
        return r['auth_deleted']

    def supportedLanguages(self):
        """
        Get the list of languages supported by this *PCloud* API server.

        :return: A dictionnary which maps supported languages codes to support languages names.

        .. seealso:: :meth:`setLanguage()`
        """
        r = self.__sendNoAuthRequest('GET', 'supportedlanguages')
        return r['languages']

    def setLanguage(self, lang):
        """
        Set the language for the user currently authenticated.

        .. note::
            This method requires the user to be authenticated.

        :param lang: A string containing the desired language code.

        .. seealso:: :meth:`supportedLanguages()`
        """
        self.__sendAuthRequest('GET', 'setlanguage', params={'language': lang})

    def listFolder(self, folder, recursive=False, showDeleted=False, noFiles=False, noShares=False):
        """
        Lists the contents of a given folder.

        .. note::
            This method requires the user to be authenticated.

        :param folder: An integer representing the id of the folder to be listed or a string giving its path.
        :param recursive: An optional boolean value indicating whether the contents of child folders should be listed as well.
        :param showDeleted: An optional boolean value indicating whether deleted files (in the trash) should be listed.
        :param noFiles: An optional boolean value indicating whether files should not be listed.
        :param noShares: An optional boolean value indicating whether shared folders or files should not be listed.
        :return: A :class:`~.info.PCloudInfo` containing the information about the given folder.
        """
        params = {}
        self.__setFolder(params, folder)

        params['recursive'] = recursive
        params['showdeleted'] = showDeleted
        params['nofiles'] = noFiles
        params['noshares'] = noShares

        r = self.__sendAuthRequest('GET', 'listfolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def createFolder(self, folder, name, exists=False):
        """
        Creates a new folder in the given folder.

        .. note::
            This method requires the user to be authenticated.

        :param folder: An integer representing the id of the folder where to create the new folder or a string giving its path.
        :param name: A string containing the name of the new folder
        :param exists: An optional boolean value indicating whether the function should raise an exception if the folder already exists.
        :return: A :class:`~.info.PCloudInfo` containing the information about the new folder.
        """
        params = {}
        self.__setFolder(params, folder)

        if 'path' in params:
            if not params['path'].endswith('/'):
                params['path'] += '/'
            params['path'] += name
        else:
            params['name'] = name

        if exists:
            r = self.__sendAuthRequest('GET', 'createfolder', params=params)
        else:
            r = self.__sendAuthRequest('GET', 'createfolderifnotexists', params=params)
        return PCloudInfo(self, r['metadata'])

    def renameFolder(self, folder, name):
        """
        Renames a folder.

        .. note::
            This method requires the user to be authenticated.

        :param folder: An integer representing the id of the folder to be renamed or a string giving its path.
        :param name: A string containing the new name for the folder.
        :return: A :class:`~.info.PCloudInfo` containing the information about the renamed folder.
        """
        params = {}
        self.__setFolder(params, folder)

        if 'path' in params:
            parts = params['path'].split('/')
            params['topath'] = '/'.join(parts[:-1] + [name])
        else:
            params['toname'] = name

        r = self.__sendAuthRequest('GET', 'renamefolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def moveFolder(self, src, dest):
        """
        Moves a folder.

        .. note::
            This method requires the user to be authenticated.

        :param src: An integer representing the id of the folder to be moved or a string giving its path.
        :param dest: An integer representing the id of the folder wehre to move the folder or a string giving its path.
        :return: A :class:`~.info.PCloudInfo` containing the information about the moved folder.
        """
        params = {}
        self.__setFolder(params, src)
        self.__setFolder(params, dest, prefix='to')

        if 'topath' in params:
            if not params['topath'].endswith('/'):
                params['topath'] += '/'
        r = self.__sendAuthRequest('GET', 'renamefolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def copyFolder(self, src, dest, overwrite=False, exist=False):
        """
        Copies a folder.

        .. note::
            This method requires the user to be authenticated.

        :param src: An integer representing the id of the folder to be copied or a string giving its path.
        :param dest: An integer representing the id of the folder wehre to copy the folder or a string giving its path.
        :param overwrite: An optional boolean value indicating whether to overwrite the contents of the destination folder.
        :param exist: An optional boolean value indicating whether the folder should not be copied if the destination already exists.
        :return: A :class:`~.info.PCloudInfo` containing the information about the copied folder.
        """
        params = {}
        self.__setFolder(params, src)
        self.__setFolder(params, dest, prefix='to')

        if 'topath' in params:
            if not params['topath'].endswith('/'):
                params['topath'] += '/'
        params['noover'] = not overwrite
        params['skipexisting'] = not exist

        r = self.__sendAuthRequest('GET', 'copyfolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def deleteFolder(self, folder):
        """
        Deletes a folder.

        .. note::
            This method requires the user to be authenticated.

        :param folder: An integer representing the id of the folder to be deleted or a string giving its path.
        :return: A :class:`~.info.PCloudInfo` containing the information about the deleted folder.
        """
        params = {}
        self.__setFolder(params, folder)

        r = self.__sendAuthRequest('GET', 'deletefolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def __setFolder(self, params, folder, prefix=''):
        if type(folder) is int:
            params[prefix + 'folderid'] = folder
        elif type(folder) is str:
            params[prefix + 'path'] = folder
        elif type(folder) is PCloudFolderInfo:
            params[prefix + 'folderid'] = folder.id
        else: #pragma: no cover
            raise TypeError(f"Invalid folder type: {type(folder)}")

    def openFile(self, file, flags=0):
        """
        Opens the given file.

        .. note::
            This method requires the user to be authenticated.


        :param file: An integer representing the id of the file to be opened or a string giving its path.
        :param flags: Optional :class:`FileOpenFlags`.
        :return: :class:`.file.PCloudFile` respesenting the opened file.

        .. seealso:: :meth:`createFile()`, :meth:`closeFile()`
        """
        params = {}
        self.__setFile(params, file)

        if not (flags & PCloud.FileOpenFlags.O_TRUNC):
            params['flags'] = int(flags | PCloud.FileOpenFlags.O_APPEND)
        else:
            params['flags'] = int(flags | PCloud.FileOpenFlags.O_WRITE)

        self.__sessions[0] = requests.Session()
        try:
            r = self.__sendAuthRequest('GET', 'file_open', params=params)
            self.__sessions[r['fd']] = self.__sessions[0]
        finally:
            del self.__sessions[0]
        return PCloudFile(self, r['fd'], r['fileid'])

    def createFile(self, folder, name, flags=0):
        """
        Creates a new file in the given folder.

        .. note::
            This method requires the user to be authenticated.

        :param file: An integer representing the id of the folder where to create a new file or a string giving its path.
        :param name: A string giving the name of the file to be created.
        :param flags: Optional :class:`FileOpenFlags`.
        :return: :class:`.file.PCloudFile` representing the opened file.

        .. seealso:: :meth:`openFile()`, :meth:`closeFile()`
        """
        params = {}
        self.__setFolder(params, folder)

        if 'path' in params:
            if not params['path'].endswith('/'):
                params['path'] += '/'
            params['path'] += name
        else:
            params['name'] = name

        params['flags'] = int(flags | PCloud.FileOpenFlags.O_CREAT | PCloud.FileOpenFlags.O_EXCL | PCloud.FileOpenFlags.O_WRITE)

        self.__sessions[0] = requests.Session()
        try:
            r = self.__sendAuthRequest('GET', 'file_open', params=params)
            self.__sessions[r['fd']] = self.__sessions[0]
        finally:
            del self.__sessions[0]
        return PCloudFile(self, r['fd'], r['fileid'])

    def readFile(self, fd, count, offset=None):
        """
        Read data from the given file descriptor.

        .. note::
            This method is intended to be used internally by :meth:`PCloudFile.read() <.file.PCloudFile.read()>`.

        :param fd: An integer file descriptor.
        :param count: An integer giving the number of bytes to read.
        :param offset: An optional integer giving the position where to read data in the file.
        :return: A byte array containing the data that has been read in the file
        """
        if offset is None:
            return self.__sendAuthRequest('GET', 'file_read', params={'fd': fd, 'count': count})
        else:
            return self.__sendAuthRequest('GET', 'file_pread', params={'fd': fd, 'count': count, 'offset': offset})

    def writeFile(self, fd, data, offset=None):
        """
        Write data to the given file descriptor.

        .. note::
            This method is intended to be used internally by :meth:`PCloudFile.write() <.file.PCloudFile.write()>`.

        :param fd: An integer file descriptor.
        :param data: A byte array containing the data to be written in the file.
        :param offset: An optional integer giving the position where to write the data in the file.
        :return: A byte array containing the data that has been read in the file
        """
        if offset is None:
            r = self.__sendAuthRequest('PUT', 'file_write', params={'fd': fd}, data=data)
        else:
            r = self.__sendAuthRequest('PUT', 'file_pwrite', params={'fd': fd, 'offset': offset}, data=data)
        return r['bytes']

    def truncateFile(self, fd, length):
        """
        Trunctate the given file descriptor to the given length.

        .. note::
            This method is intended to be used internally by :meth:`PCloudFile.truncate() <.file.PCloudFile.truncate()>`.

        :param fd: An integer file descriptor.
        :param length: An integer giving the length at which to truncate the file.
        """

        self.__sendAuthRequest('GET', 'file_truncate', params={'fd': fd, 'length': length})

    def sizeFile(self, fd):
        """
        Gets the size of the given file descriptor.

        .. note::
            This method is intended to be used internally by :attr:`PCloudFile.size <.file.PCloudFile.size>`.

        :param fd: An integer file descriptor.
        :return: An integer representing the size of the file in bytes.
        """
        r = self.__sendAuthRequest('GET', 'file_size', params={'fd': fd})
        return r['size']

    def offsetFile(self, fd):
        """
        Gets the position of the pointer for the given file descriptor.

        .. note::
            This method is intended to be used internally by :attr:`PCloudFile.offset <.file.PCloudFile.offset>`.

        :param fd: An integer file descriptor.
        :return: An integer representing the file pointer position (from the start of the file).
        """
        r = self.__sendAuthRequest('GET', 'file_size', params={'fd': fd})
        return r['offset']

    def seekFile(self, fd, offset, origin=0):
        """
        Sets the position of the pointer for the given file descriptor.

        .. note::
            This method is intended to be used internally by :meth:`PCloudFile.seek() <.file.PCloudFile.seek()>`.

        :param fd: An integer file descriptor.
        :param offset: An integer giving the new position of the file pointer.
        :param origin: Optional :class:`OffsetOrigin`.
        :return: An integer giving the new file pointer position (from the start of the file).
        """
        r = self.__sendAuthRequest('GET', 'file_seek', params={'fd': fd, 'offset': offset, 'whence': int(origin)})
        return r['offset']

    def closeFile(self, fd):
        """
        Closes the given file descriptor.

        :param fd: An integer file descriptor.
        """
        self.__sendAuthRequest('GET', 'file_close', params={'fd': fd})
        del self.__sessions[fd]

    def uploadFiles(self, folder, files, progressId=None, partial=True, overwrite=False):
        params = {}
        self.__setFolder(params, folder)

        if progressId is not None:
            params['progresshash'] = progressId
        params['renameifexists'] = not overwrite
        params['nopartial'] = not partial

        if (len(files) != 0):
            r = self.__sendAuthRequest('POST', 'uploadfile', params=params, files={k: (k, v) for k, v in files.items()})
            return [PCloudInfo(self, o) for o in r['metadata']]
        else:
            return []

    def statFile(self, file):
        """
        Get *PCloud* file information.

        .. note::
            This method requires the user to be authenticated.

        :param file: An integer representing the id of the folder where to create a new file or a string giving its path.
        :return: A :class:`~.info.PCloudInfo` containing the information about the moved folder.
        """
        params = {}
        self.__setFile(params, file)

        r = self.__sendAuthRequest('GET', 'stat', params=params)
        return PCloudInfo(self, r['metadata'])

    def checksumFile(self, file, algorithm=None):
        """
        Get checksum for the given file.

        If an algorithm is requested and the checksum is available, the corresponding checksum returned.
        Otherwise the most robust checksum ir returned.

        .. note::
            This method requires the user to be authenticated.

        :param file: An integer representing the id of the folder where to create a new file or a string giving its path.
        :param algorithm: An optional :class:`HashAlgorithm`
        :return: A :class:`~.info.PCloudInfo` containing the information about the moved folder.
        """
        params = {}
        self.__setFile(params, file)

        r = self.__sendAuthRequest('GET', 'checksumfile', params=params)

        # All hashing algorithms:
        if algorithm is PCloud.HashAlgorithm.ALL:
            return {algo.value: r[algo.value] for algo in PCloud.HashAlgorithm if algo.value in r}
        # Selected hashing algorithm:
        for algo in PCloud.HashAlgorithm:
            if algorithm is algo:
                try:
                    return r[algo.value]
                except KeyError:
                    warning(f'Could not find {algorithm.name} checksum. Returning best checksum')
                    pass
        # Best hashing algorithm:
        for algo in PCloud.HashAlgorithm:
            if algo is PCloud.HashAlgorithm.ALL:
                continue
            if algo.value in r:
                return r[algo.value]
        return PCloudInfo(self, r['metadata'])

    def renameFile(self, file, name):
        """
        Renames a file.

        .. note::
            This method requires the user to be authenticated.

        :param file: An integer representing the id of the file to be renamed or a string giving its path.
        :param name: A string containing the new name for the file.
        :return: A :class:`~.info.PCloudInfo` containing the information about the renamed file.
        """
        params = {}
        self.__setFile(params, file)

        if 'path' in params:
            parts = params['path'].split('/')
            params['topath'] = '/'.join(parts[:-1] + [name])
        else:
            params['toname'] = name

        r = self.__sendAuthRequest('GET', 'renamefile', params=params)
        return PCloudInfo(self, r['metadata'])

    def moveFile(self, src, dest):
        """
        Moves a file.

        .. note::
            This method requires the user to be authenticated.

        :param src: An integer representing the id of the file to be moved or a string giving its path.
        :param dest: An integer representing the id of the folder wehre to move the file or a string giving its path.
        :return: A :class:`~.info.PCloudInfo` containing the information about the moved file.
        """
        params = {}
        self.__setFile(params, src)
        self.__setFolder(params, dest, prefix='to')

        if 'topath' in params:
            if not params['topath'].endswith('/'):
                params['topath'] += '/'
        r = self.__sendAuthRequest('GET', 'renamefile', params=params)
        return PCloudInfo(self, r['metadata'])

    def copyFile(self, src, dest, overwrite=False):
        """
        Copies a file.

        .. note::
            This method requires the user to be authenticated.

        :param src: An integer representing the id of the file to be copied or a string giving its path.
        :param dest: An integer representing the id of the folder wehre to copy the file or a string giving its path.
        :param overwrite: An optional boolean value indicating whether to overwrite the contents of the destination file.
        :return: A :class:`~.info.PCloudInfo` containing the information about the copied file.
        """
        params = {}
        self.__setFile(params, src)
        self.__setFolder(params, dest, prefix='to')

        if 'topath' in params:
            if not params['topath'].endswith('/'):
                params['topath'] += '/'
        params['noover'] = not overwrite

        r = self.__sendAuthRequest('GET', 'copyfile', params=params)
        return PCloudInfo(self, r['metadata'])

    def deleteFile(self, file):
        """
        Deletes a file.

        .. note::
            This method requires the user to be authenticated.

        :param file: An integer representing the id of the file to be deleted or a string giving its path.
        :return: A :class:`~.info.PCloudInfo` containing the information about the deleted file.
        """
        params = {}
        self.__setFile(params, file)

        r = self.__sendAuthRequest('GET', 'deletefile', params=params)
        return PCloudInfo(self, r['metadata'])

    def __setFile(self, params, file, prefix=''):
        if type(file) is int:
            params[prefix + 'fileid'] = file
        elif type(file) is str:
            params[prefix + 'path'] = file
        elif type(file) is PCloudFileInfo:
            params[prefix + 'fileid'] = file.id
        else: #pragma: no cover
            raise TypeError(f"Invalid file type: {type(file)}")

    def check(self, file, checksum, algorithm=None, retry=False):
        """
        Check that the checksum of the given file is the expected one.
        If **algorithm** is not provided, the algorithm is determined based on the length of the checksum.
        If the checksums do not match, a message is displayed with the expected and the actual checksums.

        :param file: An integer representing the id of the file whose integrity to verify or a string giving its path.
        :param checksum: A string containing the expected checksum for the file.
        :param algorithm: An optional :class:`HashAlgorithm` to be used to obtain the checksum
        :parem retry: An optional boolean value indicating whether to retry in case of "File not found" error (the server needs some time to actualize its checksum cache.
        :return: A boolean value indicating whether the checksums match.
        """
        if algorithm is None:
            for algo in PCloud.HashAlgorithm:
                if (len(checksum) == algo.length):
                    algorithm = algo
                    break
            else:
                raise ValueError(f"Invalid checksum: \"{checksum}\"")

        attempts = 0
        while True:
            attempts += 1
            try:
                fileChecksum = self.checksumFile(file, algorithm)
                if (fileChecksum != checksum):
                    print(f"Checksum mismatch:\n  - Local file checksum:  {checksum}\n  - Remote file checksum: {fileChecksum}")
                return (fileChecksum == checksum)
            except PCloudError as e:
                if (e.code != 2009) or (attempts >= 6) or not retry:
                    raise e
                else:
                    time.sleep(5)

    def upload(self, srcFilePath, fileOrFolder, destFileName=None):
        """
        Upload a file.

        :param srcFilePath: A string representing the path to the file to upload.
        :param fileOrFolder: An integer representing the id of the folder where to upload the file or the file itself or a string giving its path.
        :param destFileName: An optional string giving the name of the new file.
        :yield: The current file pointer position.
        """
        progPath = srcFilePath + '.prog'

        if destFileName is not None:
            print(f'Upload {srcFilePath} to pCloud://{fileOrFolder}/{destFileName}')
        else:
            print(f'Upload {srcFilePath} to pCloud://{fileOrFolder}')

        if os.path.isfile(progPath) or (destFileName is None):
            if os.path.isfile(progPath):
                with open(progPath, 'rt') as progFile:
                    offset = int(progFile.read())
            else:
                offset = 0

            if type(fileOrFolder) is str:
                if destFileName is None:
                    file = fileOrFolder
                else:
                    file = fileOrFolder + destFileName
            else:
                file = fileOrFolder
            with open(srcFilePath, 'rb') as srcFile, self.openFile(file) as pCloudFile:
                for o in pCloudFile.uploadFile(srcFile, offset):
                    with open(progPath, 'wt') as progFile:
                        progFile.write(str(o))
                    yield o
        else:
            with open(srcFilePath, 'rb') as srcFile, self.createFile(fileOrFolder, destFileName) as pCloudFile:
                for o in pCloudFile.uploadFile(srcFile, 0):
                    with open(progPath, 'wt') as progFile:
                        progFile.write(str(o))
                    yield o

        print(f'remove("{progPath}")')
        os.remove(progPath)

    def download(self, destFilePath, file):
        """
        Donwload a file.

        :param destFilePath: A string representing the path where to donwload the file.
        :param fileOrFolder: An integer representing the id of the file to download or a string giving its path.
        :yield: The current file pointer position.
        """
        progPath = destFilePath + '.prog'

        print(f'Download pCloud://{file} to {destFilePath}')

        offset = 0
        if os.path.isfile(progPath):
            with open(progPath, 'rt') as progFile:
                offset = int(progFile.read())
            mode = 'ab'
        else:
            mode = 'xb'

        with open(destFilePath, mode) as destFile, self.openFile(file) as pCloudFile:
            for o in pCloudFile.downloadFile(destFile, offset):
                with open(progPath, 'wt') as progFile:
                    progFile.write(str(o))
                yield o

        print(f'remove("{progPath}")')
        os.remove(progPath)

    def __sendAuthRequest(self, method, endPoint, params=None, data=None, files=None):
        if params is None:
            params = {}
        if self.__authtoken is not None:
            params['auth'] = self.__authtoken
        else:
            if self.username is None:
                raise ValueError("PCloud username is not set")
            if self.password is None:
                raise ValueError("PCloud password is not set")

            digest = self.getDigest()

            usernameSha1Hash = sha1()
            usernameSha1Hash.update(self.username.lower().encode())

            sha1Hash = sha1()
            sha1Hash.update(self.password.encode())
            sha1Hash.update(usernameSha1Hash.hexdigest().encode())
            sha1Hash.update(digest.encode())

            params['username']       = self.username
            params['digest']         = digest
            params['passworddigest'] = sha1Hash.hexdigest()
            params['getauth']        = 1
            params['logout']         = 1

        r = self.__sendRequest(method, endPoint, params=params, data=data, files=files)
        try:
            self.__authtoken = r['auth']
            del r['auth']
        except KeyError:
            pass
        except TypeError:
            return r
        r.raise_for_status()
        return r

    def __sendNoAuthRequest(self, method, endPoint, params=None, data=None, files=None):
        r = self.__sendRequest(method, endPoint, params=params, data=data, files=files)
        r.raise_for_status()
        return r

    def __sendRequest(self, method, endPoint, params=None, data=None, files=None):
        kwArgs = {}
        if params is not None:
            kwArgs['params'] = params
        if type(data) is bytes:
            kwArgs['data'] = data
        if type(files) is dict:
            kwArgs['files'] = files

        # Initialize PCloud server list
        if (len(self.__hostnames) == 0):
            self.__hostnames = [PCloud.defaultServer]
            try:
                self.__hostnames = self.getApiServer() + [PCloud.defaultServer]
            except:
                pass

        # Get session if any
        if (params is not None) and ('fd' in params):
            s = self.__sessions[params['fd']]
        else:
            try:
                s = self.__sessions[0]
            except KeyError:
                s = requests

        # TODO try other servers if it fails
        h = 0
        #print(f"{self.__hostnames[h] + endPoint} {kwArgs}")
        r = s.request(method, self.__hostnames[h] + endPoint, **kwArgs)

        r.raise_for_status()
        if r.headers['Content-Type'].startswith('application/json'):
            #print(r.json())
            return PCloudResponse(r.json())
        elif (r.headers['Content-Type'] == 'application/octet-stream'):
            #print(r.content)
            return r.content
        else: #pragma: no cover
            raise ValueError(f"Unhandled content type: {r.headers['Content-Type']}")
