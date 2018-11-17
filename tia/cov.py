"""
Functionality to access coveragepy v5.03a coverage databases (schema v2).
"""

from sqlite3.dbapi2 import connect, Cursor
from contextlib import contextmanager
from typing import NamedTuple, Iterator


class FileTableRow(NamedTuple):
    file_id: int
    path: str


class ContextTableRow(NamedTuple):
    context_id: int
    context: str


class LineTableRow(NamedTuple):
    file_id: int
    context_id: int
    lineno: int


@contextmanager
def database_cursor(database_path: str) -> Iterator[Cursor]:
    connection = connect(database_path)
    cursor = connection.cursor()
    try:
        yield cursor  # yields a cursor instead of a connection
    finally:
        cursor.close()
        connection.close()


def _get_file_table(cursor: Cursor) -> Iterator[FileTableRow]:
    cursor.execute("SELECT * FROM file")
    rows = cursor.fetchall()
    for row in rows:
        yield FileTableRow(*row)


def _get_context_table(cursor: Cursor) -> Iterator[ContextTableRow]:
    # TODO: Clarify which dynamic contexts are possible. Provide info about
    # required post processing of content like e.g.:
    # (1, '')
    # ...
    # (13, 'testsfailed')
    cursor.execute("SELECT * FROM context")
    rows = cursor.fetchall()
    for row in rows:
        yield ContextTableRow(*row)


def _get_line_table(cursor: Cursor) -> Iterator[LineTableRow]:
    cursor.execute("SELECT * FROM line")
    rows = cursor.fetchall()
    for row in rows:
        yield LineTableRow(*row)
