from pathlib import Path

from strictyaml import YAML, Any, Bool, Enum, Map, Optional, Seq, Str, load
from strictyaml.exceptions import YAMLValidationError

CONFIG_FILE_NAME: str = 'tia.yaml'


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
    pipelines_schema = Map({
        "pipelines":
        Seq(
            Map({
                "name":
                Str(),
                "type":
                Enum(["test", "analyzer"]),
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
