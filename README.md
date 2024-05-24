# PyQvd

> Utility library for reading/writing Qlik View Data (QVD) files in Python.

The _PyQvd_ library provides a simple API for reading/writing Qlik View Data (QVD) files in Python.
Using this library, it is possible to parse the binary QVD file format and convert it to a Python object
structure or vice versa.

---

- [Install](#install)
- [Usage](#usage)
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

For a detailed overview of the library's API, please refer to the
[documentation](https://pyqvd.readthedocs.io). Below is a quick example how to use _PyQvd_.

```python
from pyqvd import QvdTable

tbl = QvdTable.from_qvd("path/to/file.qvd")
print(tbl.head())
```

The above example loads the _PyQvd_ library and parses an example QVD file. A QVD file is typically
loaded using the static `QvdTable.from_qvd` function of the `QvdTable` class itself. After loading
the file's content, numerous methods and properties are available to work with the parsed data.

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
