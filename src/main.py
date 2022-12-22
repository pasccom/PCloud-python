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
    class HashAlgorithm(Enum):
        def __new__(cls, value, length=None):
            print(cls)
            obj = super(Enum, cls).__new__(cls)
            obj._value_ = value
            obj.length = length
            return obj

        SHA256 = ('sha256', 64)
        SHA1   = ('sha1',   40)
        MD5    = ('md5',    32)
        ALL    = ('all',      )


    class FileOpenFlags(IntFlag):
        O_WRITE  = 0x0002
        O_CREAT  = 0x0040
        O_EXCL   = 0x0080
        O_TRUNC  = 0x0200
        O_APPEND = 0x0400


    class OffsetOrigin(Enum):
        Begin   = 0
        Current = 1
        End     = 2

        def __int__(self):
            return self.value


    defaultServer = 'https://eapi.pcloud.com/'

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
        return (self.__authtoken is not None)

    def currentServer(self):
        return self.__sendNoAuthRequest('GET', 'currentserver')

    def getApiServer(self, binary=False):
        r = self.__sendNoAuthRequest('GET', 'getapiserver')
        if binary:
            return ['https://' + host + '/' for host in r['binapi']]
        else:
            return ['https://' + host + '/' for host in r['api']]

    def getIp(self):
        r = self.__sendNoAuthRequest('GET', 'getip')
        return r['ip']

    def getDigest(self):
        r = self.__sendNoAuthRequest('GET', 'getdigest')
        return r['digest']

    def userInfo(self):
        return self.__sendAuthRequest('GET', 'userinfo')

    def logout(self):
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
        r = self.__sendNoAuthRequest('GET', 'supportedlanguages')
        return r['languages']

    def setLanguage(self, lang):
        self.__sendAuthRequest('GET', 'setlanguage', params={'language': lang})

    def listFolder(self, folder, recursive=False, showDeleted=False, noFiles=False, noShares=False):
        params = {}
        self.__setFolder(params, folder)

        params['recursive'] = recursive
        params['showdeleted'] = showDeleted
        params['nofiles'] = noFiles
        params['noshares'] = noShares

        r = self.__sendAuthRequest('GET', 'listfolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def createFolder(self, folder, name, exists=False):
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
        params = {}
        self.__setFolder(params, src)
        self.__setFolder(params, dest, prefix='to')

        if 'topath' in params:
            if not params['topath'].endswith('/'):
                params['topath'] += '/'
        r = self.__sendAuthRequest('GET', 'renamefolder', params=params)
        return PCloudInfo(self, r['metadata'])

    def copyFolder(self, src, dest, overwrite=False, exist=False):
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
        else:
            raise TypeError(f"Invalid folder type: {type(folder)}")

    def openFile(self, file, flags=0):
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
        if offset is None:
            return self.__sendAuthRequest('GET', 'file_read', params={'fd': fd, 'count': count})
        else:
            return self.__sendAuthRequest('GET', 'file_pread', params={'fd': fd, 'count': count, 'offset': offset})

    def writeFile(self, fd, data, offset=None):
        if offset is None:
            r = self.__sendAuthRequest('PUT', 'file_write', params={'fd': fd}, data=data)
        else:
            r = self.__sendAuthRequest('PUT', 'file_pwrite', params={'fd': fd, 'offset': offset}, data=data)
        return r['bytes']

    def truncateFile(self, fd, length):
        self.__sendAuthRequest('GET', 'file_truncate', params={'fd': fd, 'length': length})

    def sizeFile(self, fd):
        r = self.__sendAuthRequest('GET', 'file_size', params={'fd': fd})
        return r['size']

    def offsetFile(self, fd):
        r = self.__sendAuthRequest('GET', 'file_size', params={'fd': fd})
        return r['offset']

    def seekFile(self, fd, offset, origin=0):
        r = self.__sendAuthRequest('GET', 'file_seek', params={'fd': fd, 'offset': offset, 'whence': int(origin)})
        return r['offset']

    def closeFile(self, fd):
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
        params = {}
        self.__setFile(params, file)

        r = self.__sendAuthRequest('GET', 'stat', params=params)
        return PCloudInfo(self, r['metadata'])

    def checksumFile(self, file, algorithm=None):
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
        params = {}
        self.__setFile(params, src)
        self.__setFolder(params, dest, prefix='to')

        if 'topath' in params:
            if not params['topath'].endswith('/'):
                params['topath'] += '/'
        r = self.__sendAuthRequest('GET', 'renamefile', params=params)
        return PCloudInfo(self, r['metadata'])

    def copyFile(self, src, dest, overwrite=False):
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
        else:
            raise TypeError(f"Invalid file type: {type(file)}")

    def check(self, file, checksum, algorithm=None, retry=False):
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
        progPath = srcFilePath + '.prog'

        if destFileName is not None:
            print(f'Upload {srcFilePath} to pCloud://{fileOrFolder + destFileName}')
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
        else:
            raise ValueError(f"Unhandled content type: {r.headers['Content-Type']}")
