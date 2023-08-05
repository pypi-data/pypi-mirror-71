# Constants that will be used throughout the Windows API functions

from enum import IntEnum, IntFlag


MIN_HANDLE = 0x80               # Max the lowest handle reasonable
MAX_HANDLE = 0xFFFFFFFF - 1     # set the highest handle value

# File creation disposition
CREATE_NEW = 1
CREATE_ALWAYS = 2
OPEN_EXISTING = 3
OPEN_ALWAYS = 4
TRUNCATE_EXISTING = 5

# File access constants
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000

# File share mode
FILE_SHARE_READ = 1
FILE_SHARE_WRITE = 2
FILE_SHARE_DELETE = 4

# Standard success stats
ERROR_SUCCESS = 0

# Registry view
KEY_WOW64_32KEY = 0x0200
KEY_WOW64_64KEY = 0x0100

# Registry disposition
REG_CREATED_NEW_KEY = 1
REG_OPENED_EXISTING_KEY = 2


class RegistryKey(IntEnum):
    """Predefined keys in winreg.h"""
    HKEY_CLASSES_ROOT = 0x80000000
    HKEY_CURRENT_USER = 0x80000001
    HKEY_LOCAL_MACHINE = 0x80000002
    HKEY_USERS = 0x80000003
    HKEY_PERFORMANCE_DATA = 0x80000004
    HKEY_CURRENT_CONFIG = 0x80000005
    HKEY_DYN_DATA = 0x80000006
    HKEY_PERFORMANCE_TEXT = 0x80000050
    HKEY_PERFORMANCE_NLSTEXT = 0x80000060


class RegistryDataType(IntEnum):
    """Registry value data types in winreg.h"""
    REG_NONE = 0
    REG_SZ = 1
    REG_EXPAND_SZ = 2
    REG_BINARY = 3
    REG_DWORD = 4
    REG_DWORD_BIG_ENDIAN = 5
    REG_LINK = 6
    REG_MULTI_SZ = 7
    REG_QWORD = 11


class ServiceAccess(IntFlag):
    """Access Rights for a Service"""
    SERVICE_ALL_ACCESS = 0xF01FF
    SERVICE_CHANGE_CONFIG = 0x0002
    SERVICE_ENUMERATE_DEPENDENTS = 0x0008
    SERVICE_INTERROGATE = 0x0080
    SERVICE_PAUSE_CONTINUE = 0x0040
    SERVICE_QUERY_CONFIG = 0x0001
    SERVICE_QUERY_STATUS = 0x0004
    SERVICE_START = 0x0010
    SERVICE_STOP = 0x0020
    SERVICE_USER_DEFINED_CONTROL = 0x0100


class ServiceType(IntFlag):
    SERVICE_ADAPTER = 0x004
    SERVICE_FILE_SYSTEM_DRIVER = 0x002
    SERVICE_KERNEL_DRIVER = 0x001
    SERVICE_RECOGNIZER_DRIVER = 0x008
    SERVICE_WIN32_OWN_PROCESS = 0x010
    SERVICE_WIN32_SHARE_PROCESS = 0x020
    SERVICE_USER_OWN_PROCESS = 0x050
    SERVICE_USER_SHARE_PROCESS = 0x060
    SERVICE_INTERACTIVE_PROCESS = 0x100


class ServiceStart(IntEnum):
    SERVICE_AUTO_START = 2
    SERVICE_BOOT_START = 0
    SERVICE_DEMAND_START = 3
    SERVICE_DISABLED = 4
    SERVICE_SYSTEM_START = 1


class Visibility(IntEnum):
    """Enums for nCmdShow parameter."""
    SW_FORCEMINIMIZE = 11
    SW_HIDE = 0
    SW_MAXIMIZE = 3
    SW_MINIMIZE = 6
    SW_RESTORE = 9
    SW_SHOW = 5
    SW_SHOWDEFAULT = 10
    SW_SHOWMAXIMIZED = 3
    SW_SHOWMINIMIZED = 2
    SW_SHOWMINNOACTIVE = 7
    SW_SHOWNA = 8
    SW_SHOWNOACTIVATE = 4
    SW_SHOWNORMAL = 1
