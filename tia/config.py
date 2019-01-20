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
    dirs: Tuple[DirConfig, ...]
    files: Tuple[FileConfig, ...]
    full_scope_command: str
    partial_scope_command: str


class AnalyzerPipelineConfigExpanded(NamedTuple):
    name: str
    files: Iterator[FileConfig]
    full_scope_command: str
    partial_scope_command: str


# TODO: fix pytest issue in case of rename to TestPipelineConfig
class PipelineConfig(NamedTuple):
    name: str
    coverage_db: str
    dirs: Tuple[DirConfig, ...]
    files: Tuple[FileConfig, ...]
    full_scope_command: str
    partial_scope_command: str


class PipelineConfigExpanded(NamedTuple):
    name: str
    coverage_db: str
    files: Iterator[FileConfig]
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
            directories_immutable = tuple(directories)
        except:
            pass  # dirs are optional
        try:
            files = [FileConfig(d["path"].value, d["full-scope"].value) for d in p["files"]]
            files_immutable = tuple(files)
        except:
            pass  # files are optional
        if p['type'].value == 'test':
            coverage_db = p["coverage"].value
            pipeline_config = PipelineConfig(
                name=name,
                coverage_db=coverage_db,
                dirs=directories_immutable,
                files=files_immutable,
                full_scope_command=full_scope_command,
                partial_scope_command=partial_scope_command)
        else:  # only other valid type is "analyzer" pipeline
            pipeline_config = AnalyzerPipelineConfig(
                name=name,
                dirs=directories_immutable,
                files=files_immutable,
                full_scope_command=full_scope_command,
                partial_scope_command=partial_scope_command)
        yield pipeline_config


# TODO: test expand_pipeline_config()
def expand_pipeline_config(pipeline_config: Union[AnalyzerPipelineConfig, PipelineConfig]
                           ) -> Union[AnalyzerPipelineConfigExpanded, PipelineConfigExpanded]:
    expanded_file_configs = []
    for d in pipeline_config.dirs:
        file_paths = expand_directory(d.path)
        for file_path in file_paths:
            file_config = FileConfig(file_path, d.full_scope)
            expanded_file_configs.append(file_config)
    # add file_configs into expanded_file_configs
    file_configs = [fc for fc in pipeline_config.files]
    file_configs.extend(expanded_file_configs)
    file_config_generator = (f for f in file_configs)
    if type(pipeline_config) is PipelineConfig:
        expanded_config = PipelineConfigExpanded(
            name=pipeline_config.name,
            coverage_db=pipeline_config.coverage_db,  # mypy: false positive
            files=file_config_generator,
            full_scope_command=pipeline_config.full_scope_command,
            partial_scope_command=pipeline_config.partial_scope_command)
    elif type(pipeline_config) is AnalyzerPipelineConfig:
        expanded_config = AnalyzerPipelineConfigExpanded(  # mypy: false positive
            name=pipeline_config.name,
            files=file_config_generator,
            full_scope_command=pipeline_config.full_scope_command,
            partial_scope_command=pipeline_config.partial_scope_command)
    else:
        ConfigError("Pipeline directories of unsupported pipeline type cannot be expanded.")
    return expanded_config
