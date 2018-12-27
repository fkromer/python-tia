"""
Functionality to access coveragepy v5.03a coverage databases (schema v2).
"""

from contextlib import contextmanager
from sqlite3.dbapi2 import Cursor, connect
from typing import Iterator, NamedTuple, Set

Id = int
Ids = Iterator[Id]

TestReference = str
Line = int

FilePath = str
FilePaths = Iterator[FilePath]

TestName = str
TestNames = Iterator[TestName]


class FileTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    file_id: Id
    path: FilePath


class ContextTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    context_id: Id
    context: TestReference


class LineTableRow(NamedTuple):  #pylint: disable=too-few-public-methods
    file_id: Id
    context_id: Id
    lineno: Line


FileTable = Iterator[FileTableRow]

ContextTable = Iterator[ContextTableRow]

LineTable = Iterator[LineTableRow]


@contextmanager
def database_cursor(database_path: str) -> Iterator[Cursor]:
    connection = connect(database_path)
    cursor = connection.cursor()
    try:
        yield cursor  # yields a cursor instead of a connection
    finally:
        cursor.close()
        connection.close()


def get_file_table(cursor: Cursor) -> FileTable:
    cursor.execute("SELECT * FROM file")
    rows = cursor.fetchall()
    for row in rows:
        yield FileTableRow(*row)


def get_context_table(cursor: Cursor) -> ContextTable:
    # TODO: Clarify which dynamic contexts are possible. Provide info about
    # required post processing of content like e.g.:
    # (1, '')
    # ...
    # (13, 'testsfailed')
    cursor.execute("SELECT * FROM context")
    rows = cursor.fetchall()
    for row in rows:
        yield ContextTableRow(*row)


def get_line_table(cursor: Cursor) -> LineTable:
    cursor.execute("SELECT * FROM line")
    rows = cursor.fetchall()
    for row in rows:
        yield LineTableRow(*row)


def get_file_ids(file_table: FileTable, file_paths: FilePaths) -> Ids:
    # return single element content of generator instead of whole generator
    for file_id, path in file_table:
        for file_path in file_paths:
            if file_path == path:
                yield file_id


def get_context_ids(line_table: LineTable, prod_file_id: Id) -> Ids:
    already_seen_contexts: Set[Id] = set()
    for file_id, context_id, _ in line_table:
        if file_id == prod_file_id:
            if context_id not in already_seen_contexts:
                already_seen_contexts.add(context_id)
                yield context_id


def get_test_name(context_table: Iterator[ContextTableRow], test_context_ids: Ids) -> TestNames:
    for context_id, context in context_table:
        for test_id in test_context_ids:
            if context_id == test_id:
                yield context
