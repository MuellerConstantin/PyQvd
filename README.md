# PyQvd

> Utility library for reading/writing Qlik View Data (QVD) files in Python.

The _PyQvd_ library provides a simple API for reading/writing Qlik View Data (QVD) files in Python.
Using this library, it is possible to parse the binary QVD file format and convert it to a Python object
structure or vice versa.

---

- [Install](#install)
- [Usage](#usage)
- [QVD File Format](#qvd-file-format)
  - [XML Header](#xml-header)
  - [Symbol Table](#symbol-table)
  - [Index Table](#index-table)
- [License](#license)
  - [Forbidden](#forbidden)

---

## Install

PyQvd is a Python library available through [pypi](https://pypi.org/). The recommended way to
install and maintain PyQvd as a dependency is through the package installer (PIP). Before
installing this library, download and install Python.

To use PyQvd, first install it using pip:

```bash
(.venv) $ pip install PyQvd
```

## Usage

Below is a quick example how to use _PyQvd_.

```python
from pyqvd import QvdTable

df = QvdTable.from_qvd("path/to/file.qvd")
print(df.head())
```

The above example loads the _PyQvd_ library and parses an example QVD file. A QVD file is typically
loaded using the static `QvdTable.from_qvd` function of the `QvdTable` class itself. After loading
the file's content, numerous methods and properties are available to work with the parsed data.

## QVD File Format

The *Qlik View Data (QVD)* file format is a binary file format that is used by QlikView, and
later Qlik Sense, to store data. The format is proprietary and contains one data table per file.
However, the format is well structured and can be parsed without the need of a QlikView/Qlik Sense
installation using this library. In fact, a QVD file consists of three parts: a XML header, and two
binary parts, the symbol and the index table. The XML header contains meta information about the
data table stored in the QVD file, such as the number of data records and the names of the fields.
The symbol table contains the actual distinct values for each field and the index table contains the
actual data records, consisting of references to the symbol table.

### XML Header

The XML header contains meta information about the QVD file. The header is always located at the beginning of the file and
is in human readable text format. The header contains information about the number of data records, the names of the fields,
and the data types of the fields.

### Symbol Table

The symbol table contains the actual distinct values for each field. The symbol table is a binary
table that is stored in the QVD file after the XML header. The symbol table is stored in a column-major
format, meaning that the values of each field are stored in a contiguous block of memory.

In general, QlikView/Qlik Sense can handle multiple data types, such as text strings, numbers, dates,
times, timestamps, and currencies. But on memory level, a QVD file knows only the following five
different data types. The data types stored in the QVD file are interpreted by the QlikView/Qlik Sense
application when loading the data with the help of additional meta information stored in the XML header.
This allows to store a date for example as a plain number in the QVD file, but to interpret it as a date
when loading the data into QlikView/Qlik Sense.

| Code | Type         | Description                                                                                   |
| ---- | ------------ | --------------------------------------------------------------------------------------------- |
| 1    | Integer      | signed 4-byte integer (little endian)                                                         |
| 2    | Double       | signed 8-byte IEEE floating point number (little endian)                                      |
| 4    | String       | null terminated string                                                                        |
| 5    | Dual Integer | signed 4-byte integer (little endian) followed by a null terminated string                    |
| 6    | Dual Double  | signed 8-byte IEEE floating point number (little endian) followed by a null terminated string |

Basically, the symbol table is a memory block that contains the distinct values of each field. The order
of the fields in the symbol table is the same as in the XML header. Each single value is prefixed with
a type byte that indicates the data type of the value itself.

### Index Table

The index table contains the actual data records, consisting of references to the symbol table. This means
that the index table does not contain the actual cell values, but a reference to the cell's value in the
symbol table. The index table is a binary table that is stored in the QVD file after the symbol table.
It is stored in a row-major format, meaning that the values of each record are stored in a contiguous block
of memory. To save memory, the indices of a record are stored with a bit mask instead of whole bytes per index.
Meta information about the bit mask is stored in the XML header.

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
