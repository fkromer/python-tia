from pathlib import Path

from glob import iglob
from strictyaml import YAML, Any, Bool, Enum, Map, Optional, Seq, Str, load
from strictyaml.exceptions import YAMLValidationError
from typing import Iterator

from tia.cov import FilePath  # TODO: cleanup

CONFIG_FILE_NAME: str = 'tia.yaml'

DirectoryPath = str


class ConfigError(Exception):
    pass


def read_file(file_path: str) -> str:
    """
    file_path type annotation:
    os.PathLike type annotation not ready yet https://github.com/python/mypy/issues/5667
    """
    config_file = Path(file_path)
    if not config_file.is_file():
        raise FileNotFoundError('Config file {name} not found.'.format(name=config_file.name))
    if config_file.name != CONFIG_FILE_NAME:
        raise ConfigError('Invalid config file name {name}.'.format(name=config_file.name))
    return config_file.read_text()


def read_and_validate_config(strictyaml_config: str) -> YAML:
    config_schema = Map({"pipelines": Any()})
    return load(strictyaml_config, config_schema)


def is_pipelines_config_valid(strictyaml_pipelines: YAML) -> YAML:
    """
    TODO: Refactor to test and analyzer specific config validation.
    """
    pipelines_schema = Map({
        "pipelines":
        Seq(
            Map({
                "name":
                Str(),
                "type":
                Enum(["test", "analyzer"]),
                Optional("coverage"):
                Str(),
                Optional("commands"):
                Map({
                    "partial-scope": Str(),
                    "full-scope": Str()
                }),
                Optional("dirs"):
                Seq(Map({
                    "path": Str(),
                    Optional("full-scope", default=False): Bool()
                })),
                Optional("files"):
                Seq(Map({
                    "path": Str(),
                    Optional("full-scope", default=False): Bool()
                }))
            }))
    })
    try:
        strictyaml_pipelines.revalidate(pipelines_schema)
        return True
    except YAMLValidationError:
        return False


def expand_directory(dir: DirectoryPath) -> Iterator[FilePath]:
    """
    Directories are represented as string (not pathlib.Purepath)
    due to performance and memory reasons. To ease directory expansion
    files are expected to end with a suffix containing a dot.
    """
    pattern = dir + '/**/*.*'
    for path in iglob(pattern, recursive=True):
        if path:
            yield path
