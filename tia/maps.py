"""
Functionality to get coverage and impact mappings from coveragepy database data.
To be used with tia/cov.py module.
"""

from typing import Iterator, NamedTuple

from tia.cov import (
    TestName,
    TestNames,
    FilePath,
    FilePaths,
)

from functional import seq
from functional.pipeline import Sequence


class CoverageMapSingle(NamedTuple):
    """
    File based coverage map (not line based w.r.t. production code functions)
    of single test name to potentially multiple production code files.
    """
    test: TestName
    production_code: FilePaths


CoverageMap = Sequence  # TODO: of CoverageMapSingle
"""File based coverage map (not line based) of test names to potentially multiple production code
files per test name."""


class ImpactMapSingle(NamedTuple):
    """
    File based impact map (not line based w.r.t. test code functions)
    of single production code file to potentially multiple test names
    """
    production_code: FilePath
    tests: TestNames


ImpactMap = Sequence  # TODO: of ImpactMapSingle


def get_coverage_map(context_table_rows, line_table_rows, file_table_rows, tests) -> CoverageMap:
    """
    For every test:
        test aka context -> context_table_rows -> context_id -> line_table_row -> file_paths
    """
    coverage_map = []  # TODO: get rid of temporary hashable list for later sequence generation
    # explicit caching required, otherwise raise of "IndexError: list index out of range"
    context_table_rows.cache()
    line_table_rows.cache()
    file_table_rows.cache()
    for test_name in tests:
        # TODO: make search strict and fuzzy search in separate function (SRP)
        test = context_table_rows.filter(lambda x: test_name in x.context)  # fuzzy search like filtering
        test_id = test.head().context_id
        covered_lines_rows = line_table_rows.filter(lambda x: x.context_id == test_id)
        file_ids = (l.file_id for l in covered_lines_rows)
        file_paths = set()
        for file_id in file_ids:
            covered_file_rows = file_table_rows.filter(lambda x: x.file_id == file_id)
            file_path = covered_file_rows.head().path
            file_paths.add(file_path)
        coverage_map.append(CoverageMapSingle(test_name, seq(file_paths)))
        del file_paths  # free memory from set
    return seq(coverage_map)
    del coverage_map  # free memory from list


def get_impact_map(file_table_rows, line_table_rows, context_table_rows, file_paths) -> ImpactMap:
    """
    For every file_path:
        file_path -> file_table_rows -> file_id -> line_table_row -> tests
    """
    impact_map = []  # TODO: get rid of temporary hashable list for later sequence generation
    # explicit caching required, otherwise raise of "IndexError: list index out of range"
    file_table_rows.cache()
    line_table_rows.cache()
    context_table_rows.cache()
    for file_path in file_paths:
        # TODO: make search strict and fuzzy search in separate function (SRP)
        file = file_table_rows.filter(lambda x: file_path in x.path)  # fuzzy search like filtering
        file_id = file.head().file_id
        impacted_lines_rows = line_table_rows.filter(lambda x: x.file_id == file_id)
        test_ids = (l.context_id for l in impacted_lines_rows)
        tests = set()
        for test_id in test_ids:
            impacted_context_rows = context_table_rows.filter(lambda x: x.context_id == test_id)
            test = impacted_context_rows.head().context
            # workaround for coveragepy 5.02a empty and irrelevant context entries 
            if test is not "" or not "testsfailed":
                tests.add(test)
        filter(None, tests)  # get rid of empty set element
        impact_map.append(ImpactMapSingle(file_path, seq(tests)))
        del tests  # free memory from set
    return seq(impact_map)
    del impact_map  # free memory from list
