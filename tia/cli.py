from sys import stderr
from pathlib import Path
from enum import IntEnum

import click

class ExitCode(IntEnum):
    ok = 0
    not_ok = 1


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enables debug output on stdout.')
@click.option(
    '--config-file',
    '-c',
    type=click.Path(resolve_path=True),
    default='tia.yml',
    help='Configuration file (default: tia.yml).',
)
@click.version_option()
@click.pass_context
def cli(ctx, verbose, config_file):
    ctx.obj = {
        'verbose': verbose,
    }
    if verbose:
        print('Configuration file: {}'.format(click.format_filename(config_file)))
    config_file_path = Path(config_file)
    # validation of config file path
    if not config_file_path.is_file():
        click.echo('Configuration file {} is not existing.'.format(config_file_path), err=True)
        exit(ExitCode.not_ok)
    if config_file_path.suffix not in ['.yaml', '.yml']:
        print('Configuration file {} is no YAML file.'.format(config_file_path))
        exit(ExitCode.not_ok)


@cli.command(help='Discover impact of production code on tests. \
If no production code file is provided with [CODE] the whole impact map \
(production code vs. tests) is provided on stdout.')
@click.argument('code', required=False, type=click.Path(resolve_path=True), default=None)
@click.option(
    '--coverage-database',
    '-d',
    type=click.Path(resolve_path=True),
    default='.coverage',
    help='Which coverage database shall be used? (Default: .coverage)')
@click.pass_context
def impact(ctx, code, coverage_database):
    print(code)
    print(coverage_database)
    verbose = ctx.obj['verbose'] # get options from parent command context
    if verbose:
        if code:
            print('Production code file: ', click.format_filename(code))
    coverage_database_path = Path(coverage_database)
    if not coverage_database_path.is_file():
        print('Database file {} is not existing.'.format(coverage_database_path), file=stderr)
        exit(ExitCode.not_ok)
    # validation if coverage database file path is a sqlite3 database later
