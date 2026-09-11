import os
import tempfile

from tasks.task_23.file_utils import (
    get_file_extension,
    get_filename_without_extension,
    is_valid_filename,
    join_path,
    normalize_path,
    get_file_size,
)


def test_get_file_extension():
    assert get_file_extension("document.txt") == "txt"


def test_get_file_extension_uppercase():
    assert get_file_extension("PHOTO.JPG") == "jpg"


def test_get_file_extension_multiple_dots():
    assert get_file_extension("archive.tar.gz") == "gz"


def test_get_file_extension_no_extension():
    assert get_file_extension("README") == ""


def test_get_file_extension_hidden_file():
    assert get_file_extension(".gitignore") == ""


def test_get_file_extension_invalid():
    assert get_file_extension(None) is None


def test_get_filename_without_extension():
    assert get_filename_without_extension("document.txt") == "document"


def test_get_filename_without_extension_multiple_dots():
    assert get_filename_without_extension("archive.tar.gz") == "archive.tar"


def test_get_filename_without_extension_no_extension():
    assert get_filename_without_extension("README") == "README"


def test_get_filename_without_extension_path():
    assert get_filename_without_extension("/tmp/report.pdf") == "/tmp/report"


def test_get_filename_without_extension_invalid():
    assert get_filename_without_extension(None) is None


def test_is_valid_filename_valid():
    assert is_valid_filename("hello.txt") is True


def test_is_valid_filename_empty():
    assert is_valid_filename("") is False


def test_is_valid_filename_spaces():
    assert is_valid_filename("   ") is False


def test_is_valid_filename_none():
    assert is_valid_filename(None) is False


def test_is_valid_filename_non_string():
    assert is_valid_filename(123) is False


def test_join_path():
    assert join_path("home", "user", "docs") == os.path.join(
        "home", "user", "docs"
    )


def test_join_path_two_parts():
    assert join_path("src", "main.py") == os.path.join("src", "main.py")


def test_join_path_invalid():
    assert join_path("home", None) is None


def test_join_path_empty():
    assert join_path() is None


def test_normalize_path():
    path = os.path.join("home", "user", "..", "docs")
    assert normalize_path(path) == os.path.normpath(path)


def test_normalize_path_empty():
    assert normalize_path("") is None


def test_normalize_path_invalid():
    assert normalize_path(None) is None


def test_get_file_size():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        path = f.name

    try:
        assert get_file_size(path) == 11
    finally:
        os.remove(path)


def test_get_file_size_missing():
    assert get_file_size("this_file_does_not_exist_12345.txt") is None