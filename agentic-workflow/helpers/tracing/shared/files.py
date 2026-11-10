"""Filesystem boundaries, identifiers, locking and atomic writes."""

import fcntl
import os
import re
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


def identifier(value: object) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value):
        raise ValueError(f"unsafe identifier: {value!r}")
    return value


@contextmanager
def locked(path: Path) -> Iterator[None]:
    """Serialize allocation/native capture/report refresh; locks release on process exit."""
    flags = os.O_RDONLY if Path(path).is_dir() else os.O_WRONLY | os.O_CREAT
    descriptor = os.open(path, flags, 0o666)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def write_atomic(path: Path, data: str | bytes) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb" if isinstance(data, bytes) else "w") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def local_path(root: Path, path: Path) -> Path:
    """Resolve the chosen root, rejecting aliases at every component inside it."""
    boundary = Path(root).absolute()
    try:
        relative = Path(path).absolute().relative_to(boundary)
    except ValueError:
        raise ValueError("path escapes implementation root") from None
    current = boundary.resolve()
    for part in relative.parts:
        if part == "..":
            raise ValueError("path escapes implementation root")
        current /= part
        if current.is_symlink():
            raise ValueError("path contains a filesystem alias")
    return current


def safe_destination(root: Path, path: Path) -> Path:
    path = local_path(root, path)
    # Hard links can alias host logs even when paths are contained.
    if path.exists() and path.stat().st_nlink != 1:
        raise ValueError("output aliases another file")
    return path
