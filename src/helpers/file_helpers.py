from pathlib import Path


def get_filename_without_extension(filename: str) -> str:
    """
    Removes the file extension from a filename using pathlib.
    :param filename: The full name of the file.
    :return: The filename without the extension.
    """
    return Path(filename).stem


def get_file_extension(filename: str) -> str:
    """
    Returns the file extension of the given filename using pathlib.
    :param filename: The full name of the file.
    :return: The file extension (without the leading dot).
    """
    return Path(filename).suffix.lstrip('.')
