import errno
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import AnyFSPath, FileSystem


def link(
    link_type: "str",
    from_fs: "FileSystem",
    from_path: "AnyFSPath",
    to_fs: "FileSystem",
    to_path: "AnyFSPath",
) -> None:
    if not isinstance(from_fs, type(to_fs)):
        raise OSError(errno.EXDEV, "can't link across filesystems")

    func = getattr(from_fs, link_type)
    return func(from_path, to_path)


def islink(link_type: str, fs: "FileSystem", path: "AnyFSPath") -> bool:
    if link_type == "symlink":
        return fs.is_symlink(path)
    if link_type == "hardlink":
        return fs.is_hardlink(path)
    if link_type in ("reflink", "copy"):
        return fs.iscopy(path)
    return False


def test_link(
    link_type: "str",
    from_fs: "FileSystem",
    from_file: "AnyFSPath",
    to_fs: "FileSystem",
    to_file: "AnyFSPath",
) -> bool:
    try:
        link(link_type, from_fs, from_file, to_fs, to_file)
    except OSError:
        return False
    return link_type in ("reflink", "copy") or islink(
        link_type, to_fs, to_file
    )
