# PyQvd

> Utility library for reading Qlik View Data (QVD) files in Python.

The _PyQvd_ library provides a simple API for reading Qlik View Data (QVD) files in Python. Using
this library, it is possible to parse the binary QVD file format and convert it to a Python object
structure.
> [!CAUTION]
> **End of Life (EOL)**  
> This version is no longer maintained.
>
> - No bug fixes
> - No security updates
> - No new releases
>
> Please upgrade to major version **v1**, which is actively maintained.

---

- [Install](#install)
- [Usage](#usage)
- [QVD File Format](#qvd-file-format)
  - [XML Header](#xml-header)
  - [Symbol Table](#symbol-table)
  - [Index Table](#index-table)
- [API Documentation](#api-documentation)
  - [QvdFile](#qvdfile)
    - [`@staticmethod load(path: str) -> QvdFile`](#staticmethod-loadpath-str---qvdfile)
    - [`get_row(index: int) -> list[any]`](#get_rowindex-int---listany)
    - [`get_table() -> dict[str, any]`](#get_table---dictstr-any)
- [License](#license)
  - [Forbidden](#forbidden)

---

## Install

_PyQvd_ is a Python library available through [pypi](https://pypi.org/). The recommended way to install and maintain _PyQvd_ as a dependency is through the package installer (PIP). Before installing this library, download and install Python.

You can get _PyQvd_ using the following command:

```bash
pip install PyQvd
```

## Usage

Below is a quick example how to use _PyQvd_.

```python
from pyqvd import QvdFile

qvd_file = QvdFile.load('sample.qvd')
data_table = qvd_file.get_table()
```

The above example loads the _PyQvd_ library and parses an example QVD file. A QVD file is typically loaded using the static
`QvdFile.load` function of the `QvdFile` class itself. After loading the file's content, numerous methods and properties
are available to work with the parsed data.

## QVD File Format

The QVD file format is a binary file format that is used by QlikView to store data. The format is proprietary. However,
the format is well documented and can be parsed without the need of a QlikView installation. In fact, a QVD file consists
of three parts: a XML header, and two binary parts, the symbol and the index table. The XML header contains meta information
about the QVD file, such as the number of data records and the names of the fields. The symbol table contains the actual
distinct values of the fields. The index table contains the actual data records. The index table is a list of indices
which point to values in the symbol table.

### XML Header

The XML header contains meta information about the QVD file. The header is always located at the beginning of the file and
is in human readable text format. The header contains information about the number of data records, the names of the fields,
and the data types of the fields.

### Symbol Table

The symbol table contains the distinct/unique values of the fields and is located directly after the XML header. The order
of columns in the symbol table corresponds to the order of the fields in the XML header. The length and offset of the
symbol sections of each column are also stored in the XML header. Each symbol section consist of the unique symbols of the
respective column. The type of a single symbol is determined by a type byte prefixed to the respective symbol value. The
following type of symbols are supported:

| Code | Type         | Description                                                                                   |
| ---- | ------------ | --------------------------------------------------------------------------------------------- |
| 1    | Integer      | signed 4-byte integer (little endian)                                                         |
| 2    | Float        | signed 8-byte IEEE floating point number (little endian)                                      |
| 4    | String       | null terminated string                                                                        |
| 5    | Dual Integer | signed 4-byte integer (little endian) followed by a null terminated string                    |
| 6    | Dual Float   | signed 8-byte IEEE floating point number (little endian) followed by a null terminated string |

### Index Table

After the symbol table, the index table follows. The index table contains the actual data records. The index table contains
binary indices that refrences to the values of each row in the symbol table. The order of the columns in the index table
corresponds to the order of the fields in the XML header. Hence, the index table does not contain the actual values of a
data record, but only the indices that point to the values in the symbol table.

## API Documentation

### QvdFile

The `QvdFile` class represents a finally parsed QVD file. It provides a high-level abstraction access to the QVD file content.
This includes meta information as well as access to the actual data records.

| Property         | Type  | Description                                                         |
| ---------------- | ----- | ------------------------------------------------------------------- |
| `path`           | `str` | The path to the QVD file that was parsed.                           |
| `number_of_rows` | `int` | The number of data records/rows that are contained in the QVD file. |
| `field_names`    | `str` | The names of the fields that are contained in the QVD file.         |

#### `@staticmethod load(path: str) -> QvdFile`

The static method `QvdFile.load` loads a QVD file from the given path and parses it. The method returns a promise that resolves
to a `QvdFile` instance.

#### `get_row(index: int) -> list[any]`

The method `get_row` returns the data record at the given index. The method returns an array
of the row's values. The order of the values in the array corresponds to the order of the fields in the QVD file.

#### `get_table() -> dict[str, any]`

The method `get_table` returns the entire data table of the QVD file. The method returns an object with the columns and the
actual data as properties. The columns property is an array of strings that contains the names of the fields in the QVD file,
similar to the `field_names` property. The data property is an array of arrays that contains the actual data records. The order
of the values in the inner arrays corresponds to the order of the fields in the QVD file.

## License

Copyright (c) 2024 Constantin Müller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[MIT License](https://opensource.org/licenses/MIT) or [LICENSE](LICENSE) for
more details.

### Forbidden

**Hold Liable**: Software is provided without warranty and the software
author/license owner cannot be held liable for damages.
