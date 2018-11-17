from tia.config import (read_file, read_and_validate_config, is_pipelines_config_valid, ConfigError,
                        CONFIG_FILE_NAME)
from pytest import raises
from strictyaml import YAML
from collections import OrderedDict


def test_reading_existing_valid_config_file_returns_string(tmpdir):
    cf = tmpdir.mkdir("subdir").join(CONFIG_FILE_NAME)
    expected_str = """
    some
    multi
    line
    config
    """
    cf.write(expected_str)
    file_path = str(cf)
    assert read_file(file_path) == expected_str


def test_reading_existing_invalid_config_file_raises_error(tmpdir):
    invalid_config_file = "tia.ini"
    cf = tmpdir.mkdir("subdir").join(invalid_config_file)
    file_content = "irrelevant"
    cf.write(file_content)  # required to create file
    file_path = str(cf)
    expected_str = "irrelevant"
    with raises(ConfigError):
        assert read_file(file_path) == expected_str


def test_reading_non_existing_config_file_raises_exception():
    file_path = "/nonexisting/" + CONFIG_FILE_NAME
    expected_str = "irrelevant"
    with raises(FileNotFoundError):
        assert read_file(file_path) == expected_str


def test_read_valid_parent_key_config():
    yaml_config = """
    pipelines:
    """
    assert read_and_validate_config(yaml_config) == YAML(OrderedDict([('pipelines', '')]))


def test_read_valid_explicit_full_blown_pipelines_config():
    yaml_pipelines_config = """
    pipelines:
    - name: pytest
      type: test
      commands:
        partial-scope: pytest --cov=tia {tests}
        full-scope: pytest --cov=tia tests
      dirs:
      - path:       /foo_dir
        full-scope: yes
      - path:       /bar_dir
        full-scope: no
      files:
      - path:       foo_file.py
        full-scope: yes
      - path:       bar_file.py
        full-scope: no
    - name: pylint
      type: analyzer
      commands:
        partial-scope: pylint {files}
        full-scope: pylint tia
      dirs:
      - path:       /baz_dir
        full-scope: no
      files:
      - path:       baz_file.ini
        full-scope: yes
    """
    yaml_pipelines = read_and_validate_config(yaml_pipelines_config)
    expected_yaml_instance = YAML(
        OrderedDict([('pipelines', [
            OrderedDict([('name', 'pytest'), ('type', 'test'),
                         ('commands',
                             OrderedDict([('partial-scope', 'pytest --cov=tia {tests}'), ('full-scope', 'pytest --cov=tia tests')]),
                         ),
                         ('dirs', [
                             OrderedDict([('path', '/foo_dir'), ('full-scope', True)]),
                             OrderedDict([('path', '/bar_dir'), ('full-scope', False)])
                         ]),
                         ('files', [
                             OrderedDict([('path', 'foo_file.py'), ('full-scope', True)]),
                             OrderedDict([('path', 'bar_file.py'), ('full-scope', False)])
                         ])]),
            OrderedDict([('name', 'pylint'), ('type', 'analyzer'),
                         ('commands',
                             OrderedDict([('partial-scope', 'pylint {files}'), ('full-scope', 'pylint tia')]),
                         ),
                         ('dirs', [OrderedDict([('path', '/baz_dir'), ('full-scope', False)])]),
                         ('files', [OrderedDict([('path', 'baz_file.ini'), ('full-scope',
                                                                            True)])])])
        ])]))
    assert is_pipelines_config_valid(yaml_pipelines) == True
    assert yaml_pipelines == expected_yaml_instance


def test_read_valid_implicit_full_blown_pipelines_config():
    yaml_pipelines_config = """
    pipelines:
    - name: pytest
      type: test
      dirs:
      - path:       /foo_dir
        full-scope: yes
      - path:       /bar_dir
      files:
      - path:       foo_file.py
        full-scope: yes
      - path:       bar_file.py
    - name: pylint
      type: analyzer
      dirs:
      - path:       /baz_dir
      files:
      - path:       baz_file.ini
        full-scope: yes
    """
    yaml_pipelines = read_and_validate_config(yaml_pipelines_config)
    expected_yaml_instance = YAML(
        OrderedDict([('pipelines', [
            OrderedDict([('name', 'pytest'), ('type', 'test'),
                         ('dirs', [
                             OrderedDict([('path', '/foo_dir'), ('full-scope', True)]),
                             OrderedDict([('path', '/bar_dir'), ('full-scope', False)])
                         ]),
                         ('files', [
                             OrderedDict([('path', 'foo_file.py'), ('full-scope', True)]),
                             OrderedDict([('path', 'bar_file.py'), ('full-scope', False)])
                         ])]),
            OrderedDict([('name', 'pylint'), ('type', 'analyzer'),
                         ('dirs', [OrderedDict([('path', '/baz_dir'), ('full-scope', False)])]),
                         ('files', [OrderedDict([('path', 'baz_file.ini'), ('full-scope',
                                                                            True)])])])
        ])]))
    assert is_pipelines_config_valid(yaml_pipelines) == True
    assert yaml_pipelines == expected_yaml_instance


def test_read_valid_single_pipeline_with_dirs_only_config():
    yaml_pipelines_config = """
    pipelines:
    - name: pytest
      type: test
      dirs:
      - path:       /foo_dir
        full-scope: yes
      - path:       /bar_dir
        full-scope: no
    """
    yaml_pipelines = read_and_validate_config(yaml_pipelines_config)
    expected_yaml_instance = YAML(
        OrderedDict([('pipelines', [
            OrderedDict([('name', 'pytest'), ('type', 'test'),
                         ('dirs', [
                             OrderedDict([('path', '/foo_dir'), ('full-scope', True)]),
                             OrderedDict([('path', '/bar_dir'), ('full-scope', False)])
                         ])])
        ])]))
    assert is_pipelines_config_valid(yaml_pipelines) == True
    assert yaml_pipelines == expected_yaml_instance


def test_read_valid_single_pipeline_with_files_only_config():
    yaml_pipelines_config = """
    pipelines:
    - name: pytest
      type: test
      files:
      - path:       foo_file.py
        full-scope: yes
      - path:       bar_file.py
        full-scope: no
    """
    yaml_pipelines = read_and_validate_config(yaml_pipelines_config)
    expected_yaml_instance = YAML(
        OrderedDict([('pipelines', [
            OrderedDict([('name', 'pytest'), ('type', 'test'),
                         ('files', [
                             OrderedDict([('path', 'foo_file.py'), ('full-scope', True)]),
                             OrderedDict([('path', 'bar_file.py'), ('full-scope', False)])
                         ])])
        ])]))
    assert is_pipelines_config_valid(yaml_pipelines) == True
    assert yaml_pipelines == expected_yaml_instance


def test_read_invalid_pipelines_config():
    """full-scope is not allowed in pipelines[0].dirs and
    pylint should be declared to be an analzyer pipeline
    (which of course cannot be detected during validation)."""
    yaml_pipelines_config = """
    pipelines:
    - name: pytest
      type: test
      dirs:
      - full-scope: yes
      - path:       /bar_dir
        full-scope: no
      - path:       bar_file.py
        full-scope: no
    - name: pylint
      type: analayzer
      dirs:
      - path:       /baz_dir
        full-scope: no
      files:
      - path:       baz_file.ini
        full-scope: yes
    """
    config = read_and_validate_config(yaml_pipelines_config)
    yaml_pipelines = config['pipelines']
    assert is_pipelines_config_valid(yaml_pipelines) == False
