"""
CPU EMULATOR BUILTIN FUNCTIONS

These functions are used to emulate the effects of known builtin functions.

Add any builtin functions that need to be handled below.  The function should be declared as such

# Using the same function for multiple instructions:
@builtin_func("memmove")
@builtin_func("memcpy")
def _memcpy(cpu_context, call_ip, func_name, func_args):
    print "IN memmove or memcpy"
    return 1  # Return anything to be placed into rax (or equivalent)

# Using a single function for a builtin
@builtin_func
def memmove(cpu_context, call_ip, func_name, func_args):
    print "IN memmove"

"""

import six

import logging
from contextlib import contextmanager

from . import utils
from .constants import *
from .registry import registrar

logger = logging.getLogger(__name__)


# Dictionary containing builtin function names -> function
BUILTINS = {}
builtin_func = registrar(BUILTINS, name="builtin")

# Collections of user defined hooks.
_USER_DEFINED = None


def get(func_name_or_start_ea):
    """
    Gets function hook for given function name or start address.

    :param func_name_or_start_ea: Name or start address of the function to get hook for.

    :return: A function to run.
    :rtype: function
    """
    # Convert the string to lowercase so it can match the dictionary of built-in functions
    if isinstance(func_name_or_start_ea, str):
        func_name_or_start_ea = func_name_or_start_ea.lower()

    # First check user defined hooks.
    if _USER_DEFINED and func_name_or_start_ea in _USER_DEFINED:
        return _USER_DEFINED[func_name_or_start_ea]

    # Then pull from our builtins.
    return BUILTINS.get(func_name_or_start_ea)


@contextmanager
def hooks(hooks):
    """
    Context manager used to temporarily set the given user defined function hooks
    during emulation.

    :param hooks: Dictionary of function names mapping to hook functions.
    :return:
    """
    global _USER_DEFINED
    try:
        _USER_DEFINED = hooks
        yield
    finally:
        _USER_DEFINED = None


@builtin_func("_alloca")
@builtin_func("_malloca")
def _alloca(cpu_context, func_name, func_args):
    """
    Allocates stack space

    NOTE: Our memory controller will automatically allocate pages as it writes.
    Therefore, we don't actually need to allocate anything, just provide them with
    a pointer.
    """
    (size,) = func_args
    if size:
        size = utils.align_page_up(size)
        logger.debug(" :: Allocating {} bytes of stack space.".format(size))
        # Returns a pointer to our allocated stack space.
        return cpu_context.sp - size


@builtin_func("malloc")
@builtin_func("calloc")
def malloc(cpu_context, func_name, func_args):
    """
    Allocates memory block
    """
    if func_name == "calloc":
        num, size = func_args
        size = num * size
    else:
        (size,) = func_args
    if size:
        logger.debug(" :: Allocating {} bytes of memory.".format(size))
        return cpu_context.mem_alloc(size)


@builtin_func
def new(cpu_context, func_name, func_args):
    """
    Allocates memory block
    """
    size = func_args[0]
    # If we have a second argument it's either a nothrow_value or a ptr to where they
    # want us to allocate the space.
    # Just assume its a ptr if it's not 0 since the emulator should not produce a nothrow_value correctly
    # and therefore be 0.
    # TODO: Perhaps provide more context to make a more informed decision.
    try:
        ptr = func_args[1]
    except IndexError:
        ptr = 0
    if size:
        if ptr:
            logger.debug(" :: Mapping {} bytes into 0x{:X}".format(size, ptr))
            # If a pointer was provided, just give it back to them without doing anything.
            # Our memory controller will automatically allocate pages as they are being written.
            return ptr
        else:
            logger.debug(" :: Allocating {} bytes of memory.".format(size))
            return cpu_context.mem_alloc(size)


@builtin_func
def realloc(cpu_context, func_name, func_args):
    """
    Reallocates memory block
    """
    ptr, size = func_args
    if ptr and size:
        logger.debug(" :: Reallocating 0x{:X} with {} bytes.".format(ptr, size))
        return cpu_context.mem_realloc(ptr, size)


@builtin_func
def memchr(cpu_context, func_name, func_args):
    """
    Locate character in block of memory.

    Searches within the first num bytes of the block of memory pointed by data_ptr
    for the first occurrence of value (interpreted as an unsigned char) and returns a pointer
    to it.
    """
    data_ptr, value, num = func_args
    if six.PY2:
        value = chr(value)

    ptr = cpu_context.memory.find(value, start=data_ptr, end=data_ptr + num)
    if ptr == -1:
        return 0
    else:
        return ptr


@builtin_func("memmove")
@builtin_func("memmove_s")
@builtin_func("wmemmove")
@builtin_func("wmemmove_s")
@builtin_func("memcpy")
@builtin_func("memcpy_s")
@builtin_func("wmemcpy")
@builtin_func("wmemcpy_s")
def memcpy(cpu_context, func_name, func_args):
    """
    Copies count characters from src to dst.
    """
    secure = func_name.endswith("_s")
    wide = func_name.startswith("w")
    if secure:
        dst, dst_size, src, count = func_args
        count = min(dst_size, count)
    else:
        dst, src, count = func_args

    if wide:
        count *= 2

    if dst and src:
        logger.debug(" :: Copying {} bytes from 0x{:X} to 0x{:X}".format(count, src, dst))
        cpu_context.mem_copy(src, dst, count)
        return 0 if secure else dst


@builtin_func
def memset(cpu_context, func_name, func_args):
    """
    Writes count number of ch characters to dst.
    """
    dst, ch, count = func_args
    if dst:
        logger.debug(" :: Writing {!r} * {} to 0x{:X}".format(chr(ch), count, dst))
        cpu_context.mem_write(dst, chr(ch) * count)
    return dst


@builtin_func
def memcmp(cpu_context, func_name, func_args):
    lhs, rhs, count = func_args
    if lhs and rhs:
        logger.debug(" :: Comparing the first {} bytes in 0x{:X} with 0x{:X}".format(count, lhs, rhs))
        left = cpu_context.mem_read(lhs, count)
        right = cpu_context.mem_read(rhs, count)
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0


@builtin_func("strcat")
@builtin_func("strcat_s")
@builtin_func("wcscat")
@builtin_func("wcscat_s")
@builtin_func("lstrcatA")
@builtin_func("lstrcatW")
def strcat(cpu_context, func_name, func_args):
    """
    Concatenates at most count characters from src, stopping if the null character
    is found, to the end of the null-terminated byte string pointed to by dst.
    The src[0] replaces the null terminator at the end of dst.
    """
    secure = func_name.endswith("_s")
    wide = func_name.startswith("w") or func_name.endswith("W")
    if secure:
        dst, dst_size, src = func_args
        if wide:
            dst_size *= 2
    else:
        dst, src = func_args
        dst_size = None

    if dst and src:
        logger.debug(" :: Concatenating c string in 0x{:X} to c string in 0x{:X}".format(src, dst))
        append_str = cpu_context.read_data(src, data_type=WIDE_STRING if wide else STRING)
        dest_str = cpu_context.read_data(dst, data_type=WIDE_STRING if wide else STRING)
        null_offset = dst + len(dest_str)
        if dst_size is not None:
            dst_size -= null_offset - dst
            append_str = append_str[:dst_size]
        terminator = b"\0\0" if wide else b"\0"
        cpu_context.mem_write(null_offset, append_str + terminator)
        return 0 if secure else dst


@builtin_func("strncat")
@builtin_func("strncat_s")
@builtin_func("wcsncat")
@builtin_func("wcsncat_s")
def strncat(cpu_context, func_name, func_args):
    """
    Concatenates at most count characters from src, stopping if the null character
    is found, to the end of the null-terminated byte string pointed to by dst.
    The src[0] replaces the null terminator at the end of dst.
    """
    secure = func_name.endswith("_s")
    wide = func_name.startswith("w")
    if secure:
        dst, dst_size, src, count = func_args
        if wide:
            dst_size *= 2
    else:
        dst, src, count = func_args
        dst_size = None
    if wide:
        count *= 2

    if dst and src:
        logger.debug(" :: Concatenating c string in 0x{:X} to c string in 0x{:X}".format(src, dst))
        append_str = cpu_context.read_data(src, data_type=WIDE_STRING if wide else STRING)[:count]
        dest_str = cpu_context.read_data(dst, data_type=WIDE_STRING if wide else STRING)
        null_offset = dst + len(dest_str)
        if dst_size is not None:
            dst_size -= null_offset - dst
            append_str = append_str[:dst_size]
        terminator = b"\0\0" if wide else b"\0"
        cpu_context.mem_write(null_offset, append_str + terminator)
        return 0 if secure else dst


@builtin_func
def strpbrk(cpu_context, func_name, func_args):
    """
    Locate characters in string.

    Returns a pointer to the first occurrence of str1 of any of the characters
    that are part of str2, or a null pointer if there are no matches.
    """
    str1_ptr, str2_ptr = func_args
    str1 = cpu_context.read_data(str1_ptr)
    str2 = cpu_context.read_data(str2_ptr)

    for offset, ch in enumerate(str1):
        if ch in str2:
            return str1_ptr + offset
    return 0


@builtin_func("strchr")
@builtin_func("strrchr")
def strchr(cpu_context, func_name, func_args):
    """
    Locate first or last occurrence of character in string.
    """
    string_ptr, character = func_args
    string = cpu_context.read_data(string_ptr)
    if six.PY2:
        character = chr(character)

    if func_name == "strchr":
        offset = string.find(character)
    else:
        offset = string.rfind(character)

    if offset == -1:
        return 0
    else:
        return string_ptr + offset


@builtin_func("strcpy")
@builtin_func("strcpy_s")
@builtin_func("wcscpy")
@builtin_func("wcscpy_s")
@builtin_func("lstrcpyA")
@builtin_func("lstrcpyW")
def strcpy(cpu_context, func_name, func_args):
    """
    Copies the null-terminated byte string pointed to by src, including the null terminator, to dst.
    """
    secure = func_name.endswith("_s")
    wide = func_name.startswith("w") or func_name.endswith("W")
    if secure:
        dst, dst_size, src = func_args
        if wide:
            dst_size *= 2
    else:
        dst, src = func_args
        dst_size = None

    if dst and src:
        logger.debug(" :: Copying c string in 0x{:X} to 0x{:X}".format(src, dst))
        terminator = b"\0\0" if wide else b"\0"
        src_str = cpu_context.read_data(src, data_type=WIDE_STRING if wide else STRING) + terminator
        size = len(src_str)
        if dst_size is not None:
            size = min(dst_size, size)  # limit to dst_size if secure.
        cpu_context.mem_copy(src, dst, size)
        return 0 if secure else dst


@builtin_func("strncpy")
@builtin_func("strncpy_s")
@builtin_func("wcsncpy")
@builtin_func("wcsncpy_s")
@builtin_func("lstrcpynA")
@builtin_func("lstrcpynW")
def strncpy(cpu_context, func_name, func_args):
    """
    Copies at most count characters of src (including the terminating null character) to dst
    but not any of the characters that follow the null character.
    For non-secure versions, if count is not reached, additional null characters are written to dst.
    """
    secure = func_name.endswith("_s")
    wide = func_name.startswith("w") or func_name.endswith("W")
    if secure:
        # Secure version has an extra dst_size argument used for validation, but we don't care to
        # throw errors if we don't have to!
        dst, _, src, count = func_args
    else:
        dst, src, count = func_args
    if wide:
        count *= 2

    if dst and src:
        logger.debug(" :: Copying c string in 0x{:X} to 0x{:X}".format(src, dst))
        terminator = b"\0\0" if wide else b"\0"
        src_str = cpu_context.read_data(src, data_type=WIDE_STRING if wide else STRING) + terminator
        size = min(count, len(src_str))
        cpu_context.mem_copy(src, dst, size)
        # Non-secure version also pads the rest with null characters to reach count size
        if not secure and size < count:
            # As a safety check, we shouldn't be writing more than about 0x1000 of padding.
            delta = count - size
            if delta > 0x1000:
                logger.warning(
                    " :: Attempted to write {} bytes of padding. Ignoring request and using {} bytes "
                    "of padding instead.".format(delta, 0x1000)
                )
                delta = 0x1000
            cpu_context.mem_write(src + size, b"\0" * delta)
        return 0 if secure else dst


@builtin_func
def strdup(cpu_context, func_name, func_args):
    """
    Returns a pointer to a null-terminated byte string, which is a duplicate of the string
    pointing to by str.
    """
    (str_ptr,) = func_args
    if str_ptr:
        logger.debug(" :: Copying c string in 0x{:X} to new pointer.".format(str_ptr))
        null_offset = cpu_context.memory.find(b"\0", start=str_ptr)
        size = null_offset - str_ptr
        # create new pointer
        new_ptr = cpu_context.mem_alloc(size + 1)
        # Copy at most size bytes of data then add the null terminator.
        cpu_context.mem_copy(str_ptr, new_ptr, size)
        cpu_context.mem_write(new_ptr + size, b"\0")
        return new_ptr


@builtin_func
def strndup(cpu_context, func_name, func_args):
    """
    Returns a pointer to a null-terminated byte string, which contains copies
    of at most size bytes from the string pointed to by str.
    """
    str_ptr, size = func_args
    if str_ptr:
        logger.debug(" :: Copying {} bytes of c string in 0x{:X} to new pointer.".format(size, str_ptr))
        null_offset = cpu_context.memory.find(b"\0", start=str_ptr)
        size - min(size, null_offset - str_ptr)
        # create new pointer
        new_ptr = cpu_context.mem_alloc(size + 1)
        # Copy at most size bytes of data then add the null terminator.
        cpu_context.mem_copy(str_ptr, new_ptr, size)
        cpu_context.mem_write(new_ptr + size, b"\0")
        return new_ptr


@builtin_func("strlen")
@builtin_func("strnlen_s")
@builtin_func("wcslen")
@builtin_func("wcsnlen_s")
@builtin_func("lstrlenA")
@builtin_func("lstrlenW")
def strlen(cpu_context, func_name, func_args):
    """
    Returns the length of the given null-terminated byte string.
    """
    secure = func_name.endswith("_s")
    wide = func_name.startswith("w") or func_name.endswith("W")
    if secure:
        str_ptr, strsz = func_args
    else:
        (str_ptr,) = func_args
        strsz = None

    if str_ptr:
        logger.debug(" :: Getting length of c string in 0x{:X}".format(str_ptr))
        str = cpu_context.read_data(str_ptr, data_type=WIDE_STRING if wide else STRING)
        size = len(str)
        if wide:
            size /= 2
        # For secure version, strsz is returned if the terminator was not found
        # in the first strsz characters.
        if strsz is not None and size > strsz:
            return strsz
        return size


@builtin_func
def strstr(cpu_context, func_name, func_args):
    """
    Locate substring.

    Returns a pointer to the first occurrence of str2 in str1, or a null pointer if str2 is not part of str1.
    """
    str1_ptr, str2_ptr = func_args
    str1 = cpu_context.read_data(str1_ptr)
    str2 = cpu_context.read_data(str2_ptr)

    offset = str1.find(str2)
    if offset == -1:
        return 0
    else:
        return str1_ptr + offset
