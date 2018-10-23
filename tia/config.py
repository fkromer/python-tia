from typing import AnyStr
from pathlib import Path

def read_file(file_path: AnyStr) -> str:
    """
    file_path type annotation:
    os.PathLike type annotation not ready yet https://github.com/python/mypy/issues/5667
    """
    config_file = Path(file_path)
    if not config_file.is_file():
        raise FileNotFoundError
    with open(file_path, 'r') as cf:
        config = cf.read()
    return config
