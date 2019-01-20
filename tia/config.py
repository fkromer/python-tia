from pathlib import Path

from glob import iglob
from strictyaml import YAML, Any, Bool, Enum, Map, Optional, Seq, Str, load
from strictyaml.exceptions import YAMLValidationError
from typing import Iterator, NamedTuple, Tuple, Generator, Union

from tia.cov import FilePath  # TODO: cleanup

CONFIG_FILE_NAME: str = 'tia.yaml'

DirectoryPath = str


class FileConfig(NamedTuple):
    path: str
    full_scope: bool


class DirConfig(NamedTuple):
    path: str
    full_scope: bool


class AnalyzerPipelineConfig(NamedTuple):
    name: str
    dirs: Tuple[DirConfig]
    files: Tuple[FileConfig]
    full_scope_command: str
    partial_scope_command: str


# TODO: fix pytest issue in case of rename to TestPipelineConfig
class PipelineConfig(NamedTuple):
    name: str
    coverage_db: str
    dirs: Tuple[DirConfig]
    files: Tuple[FileConfig]
    full_scope_command: str
    partial_scope_command: str


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


# TODO: Helper which verifies that dirs and files in config are valid paths
# before expanding them.


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


def get_pipeline_configs(
        strictyaml_config: YAML) -> Iterator[Union[AnalyzerPipelineConfig, PipelineConfig]]:
    pipelines = strictyaml_config['pipelines']
    for p in pipelines:
        name = p["name"].value
        full_scope_command = p["commands"]["full-scope"].value
        partial_scope_command = p["commands"]["partial-scope"].value
        try:
            directories = [DirConfig(d["path"].value, d["full-scope"].value) for d in p["dirs"]]
            directories = tuple(directories)
        except:
            pass  # dirs are optional
        try:
            files = [FileConfig(d["path"].value, d["full-scope"].value) for d in p["files"]]
            files = tuple(files)
        except:
            pass  # files are optional
        if p['type'].value == 'test':
            coverage_db = p["coverage"].value
            pipeline_config = PipelineConfig(
                name=name,
                coverage_db=coverage_db,
                dirs=directories,
                files=files,
                full_scope_command=full_scope_command,
                partial_scope_command=partial_scope_command)
        else:  # only other valid type is "analyzer" pipeline
            pipeline_config = AnalyzerPipelineConfig(
                name=name,
                dirs=directories,
                files=files,
                full_scope_command=full_scope_command,
                partial_scope_command=partial_scope_command)
        yield pipeline_config
