from file_utils import (
    list_files,
    file_exists,
    get_file_size,
    ensure_directory,
)


def test_list_files(tmp_path):
    (tmp_path / "b.txt").write_text("hello")
    (tmp_path / "a.txt").write_text("world")
    (tmp_path / "folder").mkdir()

    result = list_files(str(tmp_path))

    assert result == ["a.txt", "b.txt"]


def test_file_exists(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")

    assert file_exists(str(file_path)) is True
    assert file_exists(str(tmp_path / "missing.txt")) is False


def test_directory_is_not_file(tmp_path):
    assert file_exists(str(tmp_path)) is False


def test_get_file_size(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("hello")

    assert get_file_size(str(file_path)) == 5


def test_get_empty_file_size(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("")

    assert get_file_size(str(file_path)) == 0


def test_ensure_directory(tmp_path):
    directory = tmp_path / "new_folder"

    ensure_directory(str(directory))

    assert directory.exists()
    assert directory.is_dir()


def test_ensure_existing_directory(tmp_path):
    directory = tmp_path / "existing"
    directory.mkdir()

    ensure_directory(str(directory))

    assert directory.exists()
    assert directory.is_dir()