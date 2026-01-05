# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Dropped support for Python 3.8. Python >= 3.9 is now required.

### Fixed

- Writer optimization: Reworked symbol and index table building to avoid repeated byte concatenation.
Data is now accumulated in lists and joined once, reducing write complexity from O(N²) to O(N) and
significantly improving performance for large files.
- Reader optimization: Replaced byte-to-binary-string conversions with direct bitwise extraction,
eliminating large numbers of temporary string allocations. Header buffer construction was also
optimized using list accumulation and a single join.

## [2.2.2] - 2025-09-28

### Fixed

- Resolves bug handling TIME data type (serial number)

## [2.2.1] - 2025-02-01

### Added

- Added support for vectorization when constructing a QVD table from a pandas DataFrame.

### Fixed

- Fixed a bug that caused an exception when persisting 64-bit integers to a QVD file.

## [2.2.0] - 2024-10-26

### Added

- Custom copy methods for QVD symbol classes to speed up copying of symbol tables.
- Added support for customizing value formatting in QVD data tables during writing.
- Support reading of a QVD file in chunks to reduce memory usage. It's important to note that
this only affects the reading of the index table. The header and symbol table are still read
completely into memory.

### Changed

- Improved the performance of converting bit representations to integers during parsing
QVD index tables. This is accomplished by using strings instead of integer lists for
bit representations.
- Improved performance for QVD table concatenation when concatenating them inplace. This
is achieved by no longer deep copying the data of the table to be appended to. This only
affects the inplace concatenation.
- Improved inplace DataFrame transformations by avoiding unnecessary copying of the data
when transforming the DataFrame.

## [2.1.1] - 2024-09-04

### Fixed

- Fixed numpy type to native type conversion when parsing a QVD table from a pandas DataFrame. Formerly, this
results in an exception, because the internal logic assumed that the numpy type is a subclass of the native type.

## [2.1.0] - 2024-06-26

### Added

- Added support for pandas' `Timedelta` data type in QVD data tables during reading and writing.
- Added support for QVD's money data type in QVD data tables during reading and writing. In Python
this is represented as a `Decimal` object.

## [2.0.0] - 2024-06-09

### Added

- Added new more granular value types for QVD data tables like `IntegerValue`, `DoubleValue`,
`StringValue`, `DualIntegerValue` and `DualDoubleValue`.
- Support for dealing with advanced Qlik data types like `Date`, `Time`, `Timestamp` and `Interval`
in QVD data tables during reading and writing.
- Better type conversion support for importing and exporting QVD data tables to other in-memory
data structures like pandas' `DataFrame` or built-in Python dictionaries. Time related values
are no longer converted to strings but to the corresponding Python datetime objects and vice versa.
- Considers tags and number format while reading and writing.

### Changed

- Separate the reading and writing logic of QVD files from the QVD data table implementation.
The new classes `QvdFileReader` and `QvdFileWriter` are introduced to handle this logic.
- Provide a rich feature table implementation for QVD data tables by replacing the current
implementation (`QvdDataFrame`) with a new one (`QvdTable`). Features include better type
conversion support, easier data manipulation and more efficient data access.
- Values are now represented by more granular value classes. The original `QvdValue` class is
now abstract and serves as a base class for the new value classes.

### Removed

- Removed the `QvdDataFrame` class and its related functions. The `QvdTable` class is introduced
as a replacement.
