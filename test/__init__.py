import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from .test_pcloud import TestPCloud

from .test_getdigest import TestGetDigest
from .test_supportedlanguages import TestSupportedLanguages
from .test_getapiserver import TestGetApiServer
from .test_getcurrentserver import TestGetCurrentServer
from .test_getip import TestGetIp

from .test_setlanguage import TestSetLanguage
from .test_userinfo import TestUserInfo
from .test_listfolder import TestListFolder
from .test_createfolder import TestCreateFolder
from .test_renamefolder import TestRenameFolder
from .test_movefolder import TestMoveFolder
from .test_copyfolder import TestCopyFolder
from .test_deletefolder import TestDeleteFolder
from .test_uploadfile import TestUploadFile
from .test_checksumfile import TestChecksumFile
from .test_statfile import TestStatFile
from .test_renamefile import TestRenameFile
from .test_movefile import TestMoveFile
from .test_copyfile import TestCopyFile
from .test_deletefile import TestDeleteFile

from .test_openfile import TestOpenFile
from .test_createfile import TestCreateFile

from .test_readfile import TestReadFile
from .test_writefile import TestWriteFile
from .test_truncatefile import TestTruncateFile
from .test_sizefile import TestSizeFile
from .test_offsetfile import TestOffsetFile
from .test_seekfile import TestSeekFile

from .test_check import TestCheck
from .test_upload import TestUpload
from .test_download import TestDownload
