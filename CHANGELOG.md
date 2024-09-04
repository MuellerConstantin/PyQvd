# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added support for customizing value formatting in QVD data tables during writing.

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
