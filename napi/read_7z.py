from io import BytesIO
from typing import Optional
import py7zr
import tempfile
import os

NAPI_ARCHIVE_PASSWORD = "iBlm8NTigvru0Jr0"

def un7zip_api_response(content_7z: bytes) -> Optional[bytes]:
    try:
        buffer = BytesIO(content_7z)
        with tempfile.TemporaryDirectory() as tmpdir:
            with py7zr.SevenZipFile(buffer, mode="r", password=NAPI_ARCHIVE_PASSWORD) as archive:
                archive.extractall(path=tmpdir)

            files = os.listdir(tmpdir)
            if not files:
                return None
            first_file = os.path.join(tmpdir, files[0])
            with open(first_file, "rb") as f:
                return f.read()

    except (py7zr.exceptions.Bad7zFile,
            py7zr.exceptions.PasswordRequired,
            py7zr.exceptions.UnsupportedCompressionMethodError):
        return None
