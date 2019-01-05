import click
import pytest
from click.testing import CliRunner

from tia.cli import ExitCode, cli

pytestmark = [pytest.mark.cli, pytest.mark.integration]


def test_config_file_existing_and_valid_file_extension():
    runner = CliRunner()
    result = runner.invoke(cli, ['-v', '-c', 'tests/data/tia.yaml', 'impact'])
    # exact matching would fail in CI and on other machines e.g.
    # 'Configuration file: /home/fk/github/python-tia/tests/data/tia.yaml\n'
    assert 'Configuration file: ' and '/python-tia/tests/data/tia.yaml' in result.output
    assert result.exit_code == ExitCode.ok


def test_config_file_nonexisting():
    runner = CliRunner()
    result = runner.invoke(cli, ['-c', 'docs/tia.yaml', 'impact'])
    # TODO: ValueError: stderr not separately captured, but provided by click 7.0:
    # https://click.palletsprojects.com/en/7.x/api/#click.testing.Result.stderr
    # assert 'Configuration file ' and '/python-tia/docs/tia.yaml is not existing.' in result.stderr
    assert result.exit_code == ExitCode.not_ok


def test_config_file_invalid():
    runner = CliRunner()
    result = runner.invoke(cli, ['-c', 'tia.trash', 'impact'])
    # TODO:
    # assert 'Configuration file ' and '/python-tia/tia.yaml is no YAML file.' in result.stderr
    assert result.exit_code == ExitCode.not_ok


def test_database_file_existing_and_valid_sqlite3_file():
    runner = CliRunner()
    # valid -c option (configuration file) required
    result = runner.invoke(
        cli, ['-v', '-c', 'tests/data/tia.yaml', 'impact', '-d', 'tests/data/.coverage'])
    assert 'Database file: ' and '/tests/data/.coverage' in result.output
    assert result.exit_code == ExitCode.ok


def test_database_file_nonexisting():
    runner = CliRunner()
    # valid -c option, invalid -d option
    result = runner.invoke(cli,
                           ['-v', '-c', 'tests/data/tia.yaml', 'impact', '-d', 'docs/.coverage'])
    # TODO:
    # assert 'Database file ' and '/python-tia/docs/.coverage is not existing.' in result.stderr
    assert result.exit_code == ExitCode.not_ok


def test_impact_single_file():
    runner = CliRunner()
    # valid -c option, valid -d option, valid production code file
    result = runner.invoke(
        cli, ['-c', 'tests/data/tia.yaml', 'impact', '-d', 'tests/data/.coverage', 'tia/env.py'])
    assert "['test_is_no_ci', 'test_is_some_ci']" in result.output


def test_impact_several_files():
    runner = CliRunner()
    result = runner.invoke(cli, [
        '-c', 'tests/data/tia.yaml', 'impact', '-d', 'tests/data/.coverage', 'tia/env.py',
        'tia/config.py'
    ])
    assert "['test_is_no_ci', 'test_is_some_ci', 'test_read_invalid_pipelines_config', 'test_read_valid_explicit_full_blown_pipelines_config', 'test_read_valid_implicit_full_blown_pipelines_config', 'test_read_valid_parent_key_config', 'test_read_valid_single_pipeline_with_dirs_only_config', 'test_read_valid_single_pipeline_with_files_only_config', 'test_reading_existing_invalid_config_file_raises_error', 'test_reading_existing_valid_config_file_returns_string', 'test_reading_non_existing_config_file_raises_exception']" in result.output
    assert result.exit_code == ExitCode.ok


def test_coverage_single_file():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['-c', 'tests/data/tia.yaml', 'coverage', '-d', 'tests/data/.coverage', 'test_is_no_ci'])
    assert "['/home/fk/github/python-tia/tia/env.py']" in result.output
    assert result.exit_code == ExitCode.ok
