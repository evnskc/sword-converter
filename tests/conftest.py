import shutil
from pathlib import Path

from pytest import fixture

from sword_converter.converters.bible import Bible


@fixture
def bible(tmp_path):
    source = shutil.copy2(Path(__file__).resolve().parent / "KJV.zip", tmp_path / "KJV.zip")
    return Bible(source, "KJV")
