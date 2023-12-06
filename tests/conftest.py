import shutil
from pathlib import Path

from pytest import fixture


@fixture
def source(tmp_path):
    return shutil.copy2(Path(__file__).resolve().parent / "KJV.zip", tmp_path / "KJV.zip")


@fixture
def module():
    return "KJV"
