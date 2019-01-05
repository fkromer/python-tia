import pytest

from tia.maps import (
    get_coverage_map,
    get_impact_map,
)
from tia.cov import (
    get_file_table,
    get_context_table,
    get_line_table,
)

pytestmark = pytest.mark.integration


def test_coverage_map():
    db_path = 'tests/data/.coverage'
    changed_tests = ['test_read_valid_parent_key_config', 'test_is_no_ci']
    file_table = get_file_table(db_path)
    line_table = get_line_table(db_path)
    context_table = get_context_table(db_path)
    coverage_map = get_coverage_map(context_table, line_table, file_table, changed_tests)
    first_coverage_mapping = coverage_map.first()
    assert first_coverage_mapping.test == 'test_read_valid_parent_key_config'
    assert first_coverage_mapping.production_code == ['/home/fk/github/python-tia/tia/config.py']
    last_coverage_mapping = coverage_map.last()
    assert last_coverage_mapping.test == 'test_is_no_ci'
    assert last_coverage_mapping.production_code == ['/home/fk/github/python-tia/tia/env.py']


def test_impact_map():
    db_path = 'tests/data/.coverage'
    changed_production_code_files = ['tia/config.py', 'tia/env.py']
    file_table = get_file_table(db_path)
    line_table = get_line_table(db_path)
    context_table = get_context_table(db_path)
    impact_map = get_impact_map(file_table, line_table, context_table,
                                changed_production_code_files)

    first_impact_mapping = impact_map.first()
    assert first_impact_mapping.production_code == 'tia/config.py'
    assert sorted(first_impact_mapping.tests) == sorted([
        'test_read_valid_single_pipeline_with_dirs_only_config',
        'test_reading_existing_valid_config_file_returns_string',
        'test_read_valid_single_pipeline_with_files_only_config',
        'test_read_invalid_pipelines_config',
        'test_reading_existing_invalid_config_file_raises_error',
        'test_read_valid_parent_key_config', 'test_read_valid_explicit_full_blown_pipelines_config',
        'test_reading_non_existing_config_file_raises_exception',
        'test_read_valid_implicit_full_blown_pipelines_config'
    ])

    last_impact_mapping = impact_map.last()
    assert last_impact_mapping.production_code == 'tia/env.py'
    assert sorted(last_impact_mapping.tests) == sorted(['test_is_some_ci', 'test_is_no_ci'])
