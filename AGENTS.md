# Project Overview

Utility library for reading/writing Qlik View Data (QVD) files in Python.

PyQvd parses the proprietary, binary QVD file format used by QlikView and Qlik Sense into a
Python object structure and serializes it back again. It is a pure-Python library without
native extensions, published on PyPI as `PyQvd` and documented on
[Read the Docs](https://pyqvd.readthedocs.io).

## Functionality

A QVD file holds exactly one data table and consists of three parts: an XML header with the
table's metadata, a binary symbol table with the distinct values per field, and a binary
index table with the records as bit-packed references into the symbol table. The format is
described in detail in `docs/source/guide/qvd-file-format.rst`.

**Data Model**
`QvdTable` is the central, pandas-like data structure (`head`, `tail`, `select`, `rename`,
`get`, `set`, `append`, `drop`, …). Its cells are `QvdValue` instances, which model the five
physical QVD symbol types (`IntegerValue`, `DoubleValue`, `StringValue`, `DualIntegerValue`,
`DualDoubleValue`) and the logical types built on top of them (`DateValue`, `TimeValue`,
`TimestampValue`, `IntervalValue`, `MoneyValue`). Values are immutable.

**Reading & Writing**
`QvdFileReader` and `QvdFileWriter` read from and write to file paths (`str` or `Path`) or
arbitrary binary streams, including non-seekable ones. Reading can be chunked, in which case
an iterator of `QvdTable` instances is returned. The usual entry points are the convenience
methods on `QvdTable` (`from_qvd`, `from_stream`, `to_qvd`, `to_stream`).

**Interoperability**
`QvdTable` converts from/to plain dictionaries and, with the optional `pandas` extra, from/to
pandas DataFrames.

## Tech Stack

- **Language**: Python >= 3.9 (CI tests 3.9 – 3.13)
- **Packaging**: Poetry
- **Task Runner**: Nox (`noxfile.py`)
- **Testing**: pytest, pytest-benchmark, pyinstrument
- **Linting**: pylint (configured in `pyproject.toml`)
- **Documentation**: Sphinx, hosted on Read the Docs
- **Runtime dependencies**: `tabulate`; `pandas` as optional extra

# Project Structure

```
.
├── pyqvd/
│   ├── __init__.py           # Public API of the root package
│   ├── qvd.py                # QvdTable, QvdValue and all value types
│   └── io/
│       ├── __init__.py       # Public API of the io package
│       ├── reader.py         # QvdFileReader (header, symbol and index table parsing)
│       ├── writer.py         # QvdFileWriter and QvdFileWriterOptions
│       └── format.py         # Formatters for the logical value types
├── tests/
│   ├── data/                 # QVD fixtures (small, medium, large, damaged)
│   ├── unit/                 # Unit tests, run by default
│   ├── benchmark/            # Benchmarks (marker `benchmark`, not run by default)
│   ├── profiling/            # Profiling (marker `profiling`, not run by default)
│   └── conftest.py
├── docs/source/              # Sphinx documentation (user guide, API reference)
├── noxfile.py
├── pyproject.toml
├── CHANGELOG.md
└── CONTRIBUTING.md
```

# Development

All tasks run through Nox inside the Poetry environment:

- `poetry run nox -s tests` – unit tests (installs the `pandas` extra)
- `poetry run nox -s lint` – pylint over `pyqvd` and `tests`
- `poetry run nox -s build` – builds the package
- `poetry run nox -s docs` – builds the Sphinx documentation
- `poetry run nox -s benchmark` / `poetry run nox -s profiling` – performance measurements

A change is only done when `tests` and `lint` pass without findings. Changes to the reader or
writer hot paths must additionally be checked with `benchmark` against the previous state.

# Design Decisions

- **Python 3.9 compatibility**: The minimum supported version is 3.9, so no syntax or
  standard library features beyond it (`match`, `X | Y` type unions, `list[int]` in runtime
  annotations, …). Type hints use the `typing` module, as in the existing code.
- **Minimal dependencies**: The core has a single runtime dependency (`tabulate`). pandas is
  an optional extra and must only be imported where it is actually needed. Adding a new
  runtime dependency requires a very good reason and has to be discussed first.
- **Stable public API**: The public API is what `pyqvd/__init__.py` and `pyqvd/io/__init__.py`
  export. Changes on `main` must be compatible with the latest stable release – no breaking
  changes without a new major version (see `CONTRIBUTING.md`).
- **Immutable values**: `QvdValue` instances are immutable, which the library relies on (e.g.
  cached hashing). Never mutate a value in place; create a new one.
- **Format fidelity first**: Files written by PyQvd must stay loadable by QlikView/Qlik Sense
  and files read must match what Qlik would load. Do not guess about the format – base
  changes on `docs/source/guide/qvd-file-format.rst`, existing fixtures and verified behavior.
  When in doubt, ask instead of assuming.
- **Performance matters**: Reader and writer are performance-critical and have been optimized
  deliberately (bitwise extraction, list accumulation instead of byte concatenation, …). Do
  not trade these optimizations for readability without measuring.
- **Deliberately disabled lint checks**: The size and structure checks disabled in
  `pyproject.toml` reflect the inherently branch-heavy format handling. Everything else must
  pass; don't silence new findings with inline `# pylint: disable` comments without a reason.

## Coding Principles

- **KISS**: Prefer the simplest solution that works. Avoid unnecessary abstractions – extract only after the third repetition (Rule of Three).
- **DRY**: Define logic once, import everywhere. Duplicated code is a maintenance liability.
- **YAGNI**: Don't build features or abstractions on speculation. Implement what's needed now.
- **Single Responsibility**: Each function, class, and module has one clear purpose.
- **Fail Fast**: Validate inputs early, raise meaningful errors immediately. Never swallow exceptions silently.
- **Guard Clauses over Nesting**: Prefer early returns over deeply nested `if/else` blocks.
- **Explicit over Implicit**: Prefer explicit parameters and return types over hidden assumptions or side effects.
- **No Comment Spam**: Document _why_, not _what_. Docstrings on public APIs are welcome; `# increment counter` before `counter += 1` is not.
- **Docstrings in reST**: Every module, class and public function has a docstring using Sphinx field lists (`:param:`, `:return:`), as they feed the API reference.

## General Instructions

- Prefer reading before writing – understand the existing structure before generating new files or refactoring. Don't assume conventions; verify them.
- Never dig into `.venv/`, `.nox/`, `dist/` or other generated directories – if you need to understand a dependency, read its docs. If you still need additional information just ask me.
- Don't fix what you didn't break – scope changes strictly to what was asked. No opportunistic refactors, formatting fixes, or "while I'm here" changes. But if
  you find something feel free to tell me.
- One task at a time – complete and verify the current task before moving to the next. Don't batch unrelated changes in one go.
- Every bugfix comes with a test that reproduces the bug. Don't modify the QVD fixtures in `tests/data/` without being asked.
- Comments explain the code and the decisions behind it, not the discussion that led to a change. That belongs in the commit message or the issue.
- User-facing changes get an entry in an `[Unreleased]` section at the top of `CHANGELOG.md` (Keep a Changelog format; create the section if missing).
- English is the project language for code, comments, docs and commit messages. Commit messages follow the convention in `CONTRIBUTING.md`.
