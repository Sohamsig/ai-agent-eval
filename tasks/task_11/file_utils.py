import os


def list_files(directory):
    """Return sorted file names in a directory.

    Directories are ignored.
    """
    return sorted(
        name
        for name in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, name))
    )


def file_exists(path):
    """Return True if path exists and is a file."""
    return os.path.isfile(path)


def get_file_size(path):
    """Return the size of a file in bytes."""
    return os.path.getsize(path)


def ensure_directory(path):
    """Create a directory if it does not already exist."""
    os.makedirs(path, exist_ok=True)