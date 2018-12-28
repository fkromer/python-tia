"""
Functionality to access coveragepy v5.03a coverage databases (schema v2).
"""

from functional import seq
from typing import Iterator, NamedTuple

Id = int
Ids = Iterator[Id]

TestReference = str
Line = int
Lines = Iterator[Line]

FilePath = str
FilePaths = Iterator[FilePath]

TestName = str
TestNames = Iterator[TestName]


class FileTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    file_id: Id
    path: FilePath

FileTable = Iterator[FileTableRow]

class ContextTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    context_id: Id
    context: TestReference

ContextTable = Iterator[ContextTableRow]

class LineTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    file_id: Id
    context_id: Id
    lineno: Line

LineTable = Iterator[LineTableRow]


def get_file_table(db_path: str) -> FileTable:
    file_table_rows = seq.sqlite3(db_path, 'SELECT * FROM file').map(lambda x: FileTableRow(*x))
    return file_table_rows


def get_context_table(db_path: str) -> ContextTable:
    context_table_rows = seq.sqlite3(db_path, 'SELECT * FROM context').map(lambda x: ContextTableRow(*x))
    return context_table_rows


def get_line_table(db_path: str) -> LineTable:
    line_table_rows = seq.sqlite3(db_path, 'SELECT * FROM line').map(lambda x: LineTableRow(*x))
    return line_table_rows
