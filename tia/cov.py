"""
Functionality to access coveragepy v5.03a coverage databases (schema v2).
"""

from functional import seq
from typing import Iterator, NamedTuple

from functional.pipeline import Sequence

Id = int
Ids = Sequence  # TODO: of Ids

TestReference = str
Line = int
Lines = Sequence  # TODO: of Lines

FilePath = str
FilePaths = Sequence  # TODO: of FilePaths

TestName = str
TestNames = Sequence  # TODO: of TestNames


class FileTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    file_id: Id
    path: FilePath


FileTable = Sequence


class ContextTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    context_id: Id
    context: TestReference


ContextTable = Sequence


class LineTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    file_id: Id
    context_id: Id
    lineno: Line


LineTable = Sequence


def get_file_table(db_path: str) -> FileTable:
    file_table_rows = seq.sqlite3(db_path, 'SELECT * FROM file').map(lambda x: FileTableRow(*x))
    return file_table_rows


def get_context_table(db_path: str) -> ContextTable:
    context_table_rows = seq.sqlite3(db_path, 'SELECT * FROM context').map(lambda x: ContextTableRow(*x))
    return context_table_rows


def get_line_table(db_path: str) -> LineTable:
    line_table_rows = seq.sqlite3(db_path, 'SELECT * FROM line').map(lambda x: LineTableRow(*x))
    return line_table_rows
