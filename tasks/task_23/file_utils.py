import os


def get_file_extension(filename):
    """Return the lowercase file extension without the dot."""
    if not isinstance(filename, str) or not filename:
        return None

    basename = os.path.basename(filename)

    # Hidden files such as .gitignore have no extension
    if basename.startswith(".") and basename.count(".") == 1:
        return ""

    _, extension = os.path.splitext(basename)

    return extension[1:].lower()


def get_filename_without_extension(filename):
    """Return the filename without its final extension."""
    if not isinstance(filename, str) or not filename:
        return None

    root, _ = os.path.splitext(filename)

    return root


def is_valid_filename(filename):
    """Return True if filename is a valid non-empty filename."""
    if not isinstance(filename, str):
        return False

    if not filename.strip():
        return False

    return True


def join_path(*parts):
    """Join path components safely."""
    if not parts or any(not isinstance(part, str) for part in parts):
        return None

    return os.path.join(*parts)


def normalize_path(path):
    """Normalize a filesystem path."""
    if not isinstance(path, str) or not path:
        return None

    return os.path.normpath(path)


def get_file_size(path):
    """Return file size in bytes, or None if unavailable."""
    if not isinstance(path, str) or not path:
        return None

    try:
        return os.path.getsize(path)
    except (OSError, TypeError):
        return None
