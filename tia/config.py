from typing import AnyStr

def read(file_path: AnyStr) -> str:
    """
    os.PathLike type annotation not ready yet: https://github.com/python/mypy/issues/5667
    """
    with open(file_path, 'r') as cf:
        return cf.read()
