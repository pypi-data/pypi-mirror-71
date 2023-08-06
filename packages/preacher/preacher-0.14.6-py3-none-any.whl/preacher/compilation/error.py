"""Compilation errors."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Optional, Union, Iterator


@dataclass(frozen=True)
class NamedNode:
    name: str

    def __str__(self) -> str:
        return f'.{self.name}'


@dataclass(frozen=True)
class IndexedNode:
    index: int

    def __str__(self) -> str:
        return f'[{self.index}]'


Node = Union[NamedNode, IndexedNode]
Path = List[Node]


class CompilationError(Exception):
    """Compilation errors."""

    def __init__(
        self,
        message: str,
        path: Optional[Path] = None,
        cause: Optional[Exception] = None,
    ):
        super().__init__(message)
        self._message = message
        self._path = path or []
        self._cause = cause

    @property
    def path(self) -> Path:
        return self._path

    def of_parent(self, parent_path: Path) -> CompilationError:
        return CompilationError(
            message=self._message,
            path=parent_path + self.path,
            cause=self._cause,
        )

    @staticmethod
    def wrap(error: Exception) -> CompilationError:
        return CompilationError(message=str(error), cause=error)


def render_path(path: Path) -> str:
    return ''.join(str(node) for node in path)


@contextmanager
def on_key(key: str) -> Iterator:
    try:
        yield
    except CompilationError as error:
        raise error.of_parent([NamedNode(key)])


@contextmanager
def on_index(index: int) -> Iterator:
    try:
        yield
    except CompilationError as error:
        raise error.of_parent([IndexedNode(index)])
