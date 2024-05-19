"""
Contains classes for parsing and representing QVD files.
"""

import struct
from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List, Tuple, BinaryIO, Dict, Union
from dataclasses import dataclass
from tabulate import tabulate

if TYPE_CHECKING:
    import pandas as pd

class FieldType(Enum):
    """
    Represents the type of a field in a QVD file.
    """
    UNKNOWN = 'UNKNOWN'
    ASCII = 'ASCII'
    DATE = 'DATE'
    TIMESTAMP = 'TIMESTAMP'
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    INTERVAL = 'INTERVAL'
    FIX = 'FIX'
    MONEY = 'MONEY'

@dataclass
class NumberFormat:
    """
    Represents the number format of a field in a QVD file.
    """
    type: FieldType = FieldType.UNKNOWN
    n_dec: int = 0
    use_thou: int = 0
    fmt: str = None
    dec: str = None
    thou: str = None

@dataclass
class QvdFieldHeader:
    """
    Represents the header of a field in a QVD file.
    """
    field_name: str = ""
    bit_offset: int = 0
    bit_width: int = 0
    bias: int = 0
    number_format: NumberFormat = None
    no_of_symbols: int = 0
    offset: int = 0
    length: int = 0
    comment: str = ""
    tags: List[str] = None

@dataclass
class LineageInfo:
    """
    Represents lineage information in a QVD file.
    """
    discriminator: str = ""
    statement: str = ""

@dataclass
class QvdTableHeader:
    """
    Represents the header of a QVD file.
    """
    qv_build_no: int = 0
    creator_doc: str = ""
    create_utc_time: str = ""
    source_create_utc_time: str = ""
    source_file_utc_time: str = ""
    stale_utc_time: str = ""
    table_name: str = ""
    source_file_size: int = 0
    fields: List[QvdFieldHeader] = None
    compression: str = ""
    record_byte_size: int = 0
    no_of_records: int = 0
    offset: int = 0
    length: int = 0
    comment: str = ""
    lineage: List[LineageInfo] = None

class QvdValue(metaclass=ABCMeta):
    """
    Represents a value in a QVD file.
    """
    @property
    @abstractmethod
    def display_value(self) -> object:
        """
        Returns the representational value of this QVD value. This value is used for display
        purposes.

        :return: The display value.
        """

    @property
    @abstractmethod
    def calculation_value(self) -> object:
        """
        Returns the calculation value of this QVD value. This value is used for calculations
        and sorting operations.

        :return: The calculation value.
        """

    @property
    @abstractmethod
    def byte_representation(self) -> bytes:
        """
        Returns the byte representation of this QVD value. This representation is used for
        writing the value to a QVD file.

        :return: The byte representation.
        """

    @abstractmethod
    def __eq__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is equal to another object.

        :param __value: The other object.
        :return: True if the objects are equal; otherwise, False.
        """

    def __ne__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is not equal to another object.

        :param __value: The other object.
        :return: True if the objects are not equal; otherwise, False.
        """
        return not self.__eq__(__value)

    @abstractmethod
    def __hash__(self) -> int:
        """
        Returns the hash value of this QVD value.

        :return: The hash value.
        """

    def __str__(self) -> str:
        """
        Returns a string representation of this QVD value.

        :return: The string representation.
        """
        return str(self.display_value)

class IntegerValue(QvdValue):
    """
    Represents an integer value in a QVD file.
    """
    def __init__(self, value: int):
        """
        Constructs a new integer value.

        :param value: The integer value.
        """
        self._value: int = value

    @property
    def display_value(self) -> int:
        return self._value

    @property
    def calculation_value(self) -> int:
        return self._value

    @property
    def byte_representation(self) -> bytes:
        return b"\01" + self._value.to_bytes(4, byteorder="little", signed=True)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, IntegerValue):
            return False

        return self._value == __value._value

    def __hash__(self) -> int:
        return hash(self._value)

class DoubleValue(QvdValue):
    """
    Represents a double value in a QVD file.
    """
    def __init__(self, value: float):
        """
        Constructs a new double value.

        :param value: The double value.
        """
        self._value: float = value

    @property
    def display_value(self) -> float:
        return self._value

    @property
    def calculation_value(self) -> float:
        return self._value

    @property
    def byte_representation(self) -> bytes:
        return b"\02" + struct.pack("<d", self._value)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, DoubleValue):
            return False

        return self._value == __value._value

    def __hash__(self) -> int:
        return hash(self._value)

class StringValue(QvdValue):
    """
    Represents a string value in a QVD file.
    """
    def __init__(self, value: str):
        """
        Constructs a new string value.

        :param value: The string value.
        """
        self._value: str = value

    @property
    def display_value(self) -> str:
        return self._value

    @property
    def calculation_value(self) -> str:
        return self._value

    @property
    def byte_representation(self) -> bytes:
        return b"\04" + str.encode(self._value, encoding="utf-8") + b"\0"

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, StringValue):
            return False

        return self._value == __value._value

    def __hash__(self) -> int:
        return hash(self._value)

class DualIntegerValue(QvdValue):
    """
    Represents a dual value with an integer value and a string value in a QVD file.
    """
    def __init__(self, int_value: int, string_value: str):
        """
        Constructs a new dual integer value.

        :param int_value: The integer value.
        :param string_value: The string value.
        """
        self._int_value: int = int_value
        self._string_value: str = string_value

    @property
    def display_value(self) -> str:
        return self._string_value

    @property
    def calculation_value(self) -> int:
        return self._int_value

    @property
    def byte_representation(self) -> bytes:
        return (b"\05" +
                self._int_value.to_bytes(4, byteorder="little", signed=True) +
                str.encode(self._string_value, encoding="utf-8") +
                b"\0")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, DualIntegerValue):
            return False

        return (self._int_value == __value._int_value and
                self._string_value == __value._string_value)

    def __hash__(self) -> int:
        return hash((self._int_value, self._string_value))

    def __str__(self) -> str:
        return self._string_value

class DualDoubleValue(QvdValue):
    """
    Represents a dual value with a double value and a string value in a QVD file.
    """
    def __init__(self, double_value: float, string_value: str):
        """
        Constructs a new dual double value.

        :param double_value: The double value.
        :param string_value: The string value.
        """
        self._double_value: float = double_value
        self._string_value: str = string_value

    @property
    def display_value(self) -> str:
        return self._string_value

    @property
    def calculation_value(self) -> float:
        return self._double_value

    @property
    def byte_representation(self) -> bytes:
        return (b"\06" + struct.pack("<d", self._double_value) +
                str.encode(self._string_value, encoding="utf-8") + b"\0")

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, DualDoubleValue):
            return False

        return (self._double_value == __value._double_value and
                self._string_value == __value._string_value)

    def __hash__(self) -> int:
        return hash((self._double_value, self._string_value))

class QvdTable:
    """
    Represents a table in a QVD file.
    """
    def __init__(self, data: List[List[QvdValue]], columns: List[str]):
        """
        Constructs a new QVD data frame.

        :param data: The data of the data frame.
        :param columns: The columns of the data frame.
        """
        # Ensure all records have the same number of values
        if len(set(len(row) for row in data)) > 1:
            raise ValueError("All records must have the same number of values.")

        # Ensure the number of columns matches the number of values in each record
        if len(columns) != len(data[0]):
            raise ValueError("The number of columns must match the number of values in each record.")

        self._data: List[List[QvdValue]] = data
        self._columns: List[str] = columns

    @property
    def data(self) -> List[List[QvdValue]]:
        """
        Returns the data of the data frame.

        :return: The data.
        """
        return self._data

    @property
    def columns(self) -> List[str]:
        """
        Returns the columns of the data frame.

        :return: The column names.
        """
        return self._columns

    @property
    def shape(self) -> Tuple[int, int]:
        """
        Returns the shape of the data frame.

        :return: The shape, which is a tuple containing the number of rows and columns.
        """
        return (len(self._data), len(self._columns))

    @property
    def size(self) -> int:
        """
        Return an int representing the number of elements in this object.

        :return: The number of elements in the data frame.
        """
        return len(self._data) * len(self._columns)

    @property
    def empty(self) -> bool:
        """
        Returns whether the data frame is empty.

        :return: True if the data frame is empty; otherwise, False.
        """
        return len(self._data) == 0

    def head(self, n: int = 5) -> 'QvdTable':
        """
        Returns the first n rows of the data frame.

        :param n: The number of rows to return.
        :return: The first n rows.
        """
        return QvdTable(self._data[:n], self._columns)

    def tail(self, n: int = 5) -> 'QvdTable':
        """
        Returns the last n rows of the data frame.

        :param n: The number of rows to return.
        :return: The last n rows.
        """
        return QvdTable(self._data[-n:], self._columns)

    def rows(self, *args: int) -> "QvdTable":
        """
        Returns the specified rows of the data frame.

        :param args: The row indices.
        :return: The specified rows.
        """
        return QvdTable([self._data[index] for index in args], self._columns)

    def select(self, *columns: str) -> "QvdTable":
        """
        Returns a new data frame with only the specified columns.

        :param columns: The column names.
        :return: The new data frame.
        """
        column_indices = [self._columns.index(column) for column in columns]
        return QvdTable([[row[index] for index in column_indices] for row in self._data], list(columns))

    def at(self, row: int, column: str) -> QvdValue:
        """
        Returns the value at the specified row and column, where row refers to the
        current nth record.

        :param row: The row index.
        :param column: The column name.
        :return: The value at the specified row and column.
        """
        if not isinstance(row, int):
            raise TypeError("Row must be a valid row index.")

        if not isinstance(column, str):
            raise TypeError("Column must be a valid column name.")

        return self._data[row][self._columns.index(column)]

    def get(self, key: Union[str, int]) -> List[QvdValue]:
        """
        Returns the values for the specified key. If the key is a string, the values for the
        specified column are returned. If the key is an integer, the values for the specified
        row are returned.

        :param key: The key to retrieve.
        :return: The values for the specified key.
        """
        if isinstance(key, str):
            return [row[self._columns.index(key)] for row in self._data]

        if isinstance(key, int):
            return self._data[key]

        raise TypeError("Key must be a supported/valid one.")

    def __getitem__(self, key: Union[str, int]) -> List[QvdValue]:
        """
        Returns the values for the specified key. It is a shorthand for the get method.

        :param key: The key to retrieve.
        :return: The values for the specified key.
        """
        return self.get(key)

    def __str__(self) -> str:
        """
        Returns a string representation of the data frame.

        :return: The string representation.
        """
        return tabulate(self._data, headers=self._columns)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QvdTable):
            return False

        return self._data == other._data and self._columns == other._columns

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((tuple(tuple(row) for row in self._data), tuple(self._columns)))

    def to_qvd(self, path: str):
        """
        Persists the data frame to a QVD file.

        :param path: The path to the QVD file.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.writer import QvdFileWriter

        QvdFileWriter(path, self).write()

    def to_stream(self, target: BinaryIO):
        """
        Writes the QVD file to a binary stream.

        :param target: The binary stream to write to.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.writer import QvdFileWriter

        QvdFileWriter(target, self).write()

    def to_dict(self) -> Dict[str, any]:
        """
        Converts the data frame to a dictionary.

        :return: The dictionary representation of the data frame.
        """
        return {"columns": self._columns, "data": [[value.display_value for value in row] for row in self._data]}

    def to_pandas(self) -> "pd.DataFrame":
        """
        Converts the data frame to a pandas data frame.

        :return: The pandas data frame.
        """
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "Pandas is not installed. Please install it using `pip install pandas`."
            ) from exc

        return pd.DataFrame([[value.display_value for value in row] for row in self._data], columns=self._columns)

    @staticmethod
    def from_qvd(path: str) -> "QvdTable":
        """
        Loads a QVD file and returns its data frame.

        :param path: The path to the QVD file.
        :return: The data frame of the QVD file.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.reader import QvdFileReader

        return QvdFileReader(path).read()

    @staticmethod
    def from_stream(source: BinaryIO) -> "QvdTable":
        """
        Constructs a new QVD data frame from a stream.

        :param source: The source to the QVD file.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.reader import QvdFileReader

        return QvdFileReader(source).read()

    @staticmethod
    def from_dict(data: Dict[str, any]) -> "QvdTable":
        """
        Constructs a new QVD data frame from a raw value dictionary.

        :param data: The dictionary representation of the data frame.
        :return: The QVD data frame.
        """
        def _get_symbol_from_value(value: any) -> QvdValue:
            if value is None:
                return None

            if isinstance(value, QvdValue):
                return value

            if isinstance(value, int):
                return IntegerValue(value)
            if isinstance(value, float):
                return DoubleValue(value)

            return StringValue(str(value))

        table_data = [[_get_symbol_from_value(value) for value in row] for row in data["data"]]
        return QvdTable(table_data, data["columns"])

    @staticmethod
    def from_pandas(df: "pd.DataFrame") -> "QvdTable":
        """
        Constructs a new QVD data frame from a pandas data frame.

        :param df: The pandas data frame.
        :return: The QVD data frame.
        """
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "Pandas is not installed. Please install it using `pip install pandas`."
            ) from exc

        def _get_symbol_from_value(value: any) -> QvdValue:
            if value is None or pd.isna(value):
                return None

            if isinstance(value, int):
                return IntegerValue(value)
            if isinstance(value, float):
                return DoubleValue(value)

            return StringValue(str(value))

        data = [[_get_symbol_from_value(value) for value in row] for row in df.values]
        return QvdTable(data, df.columns.tolist())
