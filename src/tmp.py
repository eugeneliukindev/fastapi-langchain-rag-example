from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from secrets import token_urlsafe
from tempfile import gettempdir


@contextmanager
def create_tmp_file_from_bytes(b: bytes, extension: str) -> Generator[Path]:
    tmp_file = Path(Path(gettempdir()) / f"{token_urlsafe(32)}.{extension}")
    tmp_file.write_bytes(b)
    yield tmp_file
    tmp_file.unlink(missing_ok=True)
