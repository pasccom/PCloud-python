class PCloudError(Exception):
    """
    Class representing *PCloud* API errors.

    :param code: *PCloud* API error code.
    """

    __messages = {
        1000: "Log in required",
        1001: "No full path or name/folderid provided",
        1002: "No full path or folderid provided",
        1004: "No fileid or path provided",
        1006: "Please provide flags",
        1007: "Invalid or closed file descriptor",
        1009: "Please provide 'offset'",
        1010: "Please provide 'length'",
        1011: "Please provide 'count'",
        1016: "No full topath or toname/tofolderid provided",
        1017: "Invalid 'folderid' provided",
        1020: "Please provide language",
        1021: "Language not supported",
        1037: "Please provide at least one of 'topath', 'tofolderid' or 'toname'",
        2000: "Log in failed",
        2001: "Invalid file/folder name",
        2002: "A component of parent directory does not exist",
        2003: "Access denied, you do not have permissions to preform this operation",
        2004: "File or folder alredy exists",
        2005: "Directory does not exist",
        2006: "Folder is not empty",
        2007: "Cannot delete the root folder",
        2008: "User is over quota",
        2009: "File not found",
        2010: "Invalid path",
        2023: "You are trying to place shared folder into another shared folder",
        2028: "There are active shares or sharerequests for this folder",
        2041: "Connection broken",
        2042: "Cannot rename the root folder",
        2043: "Cannot move a folder to a subfolder of itself",
        2119: "Can not create non-encrypted file in encrypted folder",
        2206: "Can not copy folder into itself",
        2207: "Can not copy folder to subfolder of itself",
        2208: "Target folder does not exist",
        4000: "Too many login tries from this IP address",
        5000: "Internal error, try again later",
        5001: "Internal upload error",
        5003: "Write error, try reopening the file",
        5004: "Read error, try reopening the file",
    }

    def __init__(self, code):
        self.code = code

    def __str__(self):
        try:
            msg = self.__class__.__messages[self.code]
        except KeyError:
            msg = "Unknown PCloud error"
        except BaseException as e:
            msg = repr(e)

        return f"{msg} ({self.code})"
