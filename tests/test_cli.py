import click
from click.testing import CliRunner

from tia.cli import cli, ExitCode

import pytest

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
    result = runner.invoke(cli, ['-v', '-c', 'tests/data/tia.yaml', 'impact', '-d', 'tests/data/.coverage'])
    assert 'Database file: ' and '/tests/data/.coverage' in result.output
    assert result.exit_code == ExitCode.ok


def test_database_file_nonexisting():
    runner = CliRunner()
    # valid -c option, invalid -d option
    result = runner.invoke(cli, ['-v', '-c', 'tests/data/tia.yaml', 'impact', '-d', 'docs/.coverage'])
    # TODO:
    # assert 'Database file ' and '/python-tia/docs/.coverage is not existing.' in result.stderr
    assert result.exit_code == ExitCode.not_ok


def test_impact_code():
    runner = CliRunner()
    # valid -c option, valid -d option, valid production code file
    result = runner.invoke(cli, ['-v', '-c', 'tests/data/tia.yaml', 'impact', '-d', 'tests/data/.coverage', 'tia/config.py'])
    assert 'Production code file: ' and '/python-tia/tia/config.py' in result.output
    assert result.exit_code == ExitCode.ok
