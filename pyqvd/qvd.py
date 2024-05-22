"""
Module contains the core classes and functions for dealing with QVD files. The main class is the
:class:`QvdTable` class, which represents a the internal data table of a QVD file.
"""

import struct
from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, List, Tuple, BinaryIO, Dict, Union, Literal
from dataclasses import dataclass
from tabulate import tabulate

if TYPE_CHECKING:
    import pandas as pd

class FieldType(Enum):
    """
    The possible field types of a column in a QVD file.
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
    Metadata description of a field in a QVD file.
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
    Structure of the header of a QVD file.
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
    Base class for all QVD data types. All values in a QVD file must inherit from this class.
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

    def __eq__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is equal to another object.

        :param __value: The other object.
        :return: True if the objects are equal; otherwise, False.
        """
        if not isinstance(__value, QvdValue):
            return False

        return self.calculation_value == __value.calculation_value

    def __ne__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is not equal to another object.

        :param __value: The other object.
        :return: True if the objects are not equal; otherwise, False.
        """
        return not self.__eq__(__value)

    def __lt__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is less than another object.

        :param __value: The other object.
        :return: True if this value is less than the other object; otherwise, False.
        """
        if not isinstance(__value, QvdValue):
            return NotImplemented

        return self.calculation_value < __value.calculation_value

    def __le__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is less than or equal to another object.

        :param __value: The other object.
        :return: True if this value is less than or equal to the other object; otherwise, False.
        """
        if not isinstance(__value, QvdValue):
            return NotImplemented

        return self.calculation_value <= __value.calculation_value

    def __gt__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is greater than another object.

        :param __value: The other object.
        :return: True if this value is greater than the other object; otherwise, False.
        """
        if not isinstance(__value, QvdValue):
            return NotImplemented

        return self.calculation_value > __value.calculation_value

    def __ge__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is greater than or equal to another object.

        :param __value: The other object.
        :return: True if this value is greater than or equal to the other object; otherwise, False.
        """
        if not isinstance(__value, QvdValue):
            return NotImplemented

        return self.calculation_value >= __value.calculation_value

    def __hash__(self) -> int:
        """
        Returns the hash value of this QVD value.

        :return: The hash value.
        """
        return hash(self.calculation_value)

    def __str__(self) -> str:
        """
        Returns a string representation of this QVD value.

        :return: The string representation.
        """
        return str(self.display_value)

    def __repr__(self) -> str:
        """
        Returns a string representation of this QVD value.

        :return: The string representation.
        """
        return self.__str__()

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

class DualIntegerValue(QvdValue):
    """
    Represents a dual value with an integer value and a string value in a QVD file.
    
    Dual values are used to store both a display value and a calculation value in a single field.
    This is useful when the display representation of a value is different from the calculation
    representation. For example, you may want to display a date as "MM/DD/YYYY" but store it as
    an integer value representing the number of days since a certain date.
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

class DualDoubleValue(QvdValue):
    """
    Represents a dual value with a double value and a string value in a QVD file.

    Dual values are used to store both a display value and a calculation value in a single field.
    This is useful when the display representation of a value is different from the calculation
    representation. For example, you may want to display a monetary value as "$1,000.00" but store
    it as a double value representing the number of cents.
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

class QvdTable:
    """
    Core class for representing a QVD data table.
    """
    def __init__(self, data: List[List[QvdValue]], columns: List[str]):
        """
        Constructs a new QVD data table with the specified data and columns.

        :param data: The data of the data table.
        :param columns: The columns of the data table.
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
        Returns the data of the data table.

        :return: The data.
        """
        return self._data

    @property
    def columns(self) -> List[str]:
        """
        Returns the columns of the data table.

        :return: The column names.
        """
        return self._columns

    @property
    def shape(self) -> Tuple[int, int]:
        """
        Returns the shape of the data table.

        :return: The shape, which is a tuple containing the number of rows and columns.
        """
        return (len(self._data), len(self._columns))

    @property
    def size(self) -> int:
        """
        Return an int representing the number of elements in this object.

        :return: The number of elements in the data table.
        """
        return len(self._data) * len(self._columns)

    @property
    def empty(self) -> bool:
        """
        Returns whether the data table is empty.

        :return: True if the data table is empty; otherwise, False.
        """
        return len(self._data) == 0

    def head(self, n: int = 5) -> 'QvdTable':
        """
        Returns the first n rows of the data table.

        :param n: The number of rows to return.
        :return: The first n rows.
        """
        return QvdTable(self._data[:n], self._columns)

    def tail(self, n: int = 5) -> 'QvdTable':
        """
        Returns the last n rows of the data table.

        :param n: The number of rows to return.
        :return: The last n rows.
        """
        return QvdTable(self._data[-n:], self._columns)

    def rows(self, *args: int) -> "QvdTable":
        """
        Returns the specified rows of the data table.

        :param args: The row indices.
        :return: The specified rows.
        """
        return QvdTable([self._data[index] for index in args], self._columns)

    def select(self, *columns: str) -> "QvdTable":
        """
        Returns a new data table with only the specified columns.

        :param columns: The column names.
        :return: The new data table.
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

        if row < 0 or row >= len(self._data):
            raise IndexError("Row index out of range")

        if column not in self._columns:
            raise KeyError(f"Column '{column}' not found")

        return self._data[row][self._columns.index(column)]

    # pylint: disable-next=line-too-long
    def set(self, key: Union[str, int, slice, Tuple[int, str]], value: Union[QvdValue, List[QvdValue], List[List[QvdValue]]]) -> None:
        """
        Sets the value for the specified key. As a shorthand, you can also use the indexing
        operator to set values.

        :param key: The key to set.
        :param value: The value to set.

        Examples
        --------
        You can pass a single integer to overwrite a row at the specified index:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.set(0, [10, 11, 12]) # Alias tbl[0] = [10, 11, 12]
            >>> tbl
            A    B    C
            ---  ---  ---
            10   11   12
            4    5    6
            7    8    9
        
        You can pass a single string to overwrite a column with the specified name:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.set("A", [13, 14, 15]) # Alias tbl["A"] = [13, 14, 15]
            >>> tbl
            A    B    C
            ---  ---  ---
            13   2    3
            14   5    6
            15   8    9

        If you pass a column name that does not exist, a new column is added:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.set("D", [16, 17, 18]) # Alias tbl["D"] = [16, 17, 18]
            >>> tbl
            A    B    C    D
            ---  ---  ---  ---
            1    2    3    16
            4    5    6    17
            7    8    9    18

        You can pass a tuple with an integer and a string to overwrite a value at the specified row and column:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.set((0, "A"), 16) # Alias tbl[0, "A"] = 16
            >>> tbl
            A    B    C
            ---  ---  ---
            16   2    3
            4    5    6
            7    8    9

        You can pass a slice to overwrite a subset of the data table:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.set(slice(0, 2), 17) # Alias tbl[0:2] = 17
            >>> tbl
            A    B    C
            ---  ---  ---
            17   17   17
            17   17   17
            7    8    9
        """
        # Set by row and column index
        if isinstance(key, tuple):
            if not isinstance(value, QvdValue):
                raise ValueError("Value must be a QVD value.")

            if not isinstance(key[0], int):
                raise TypeError("Row must be a valid row index.")

            if not isinstance(key[1], str):
                raise TypeError("Column must be a valid column name.")

            if key[0] < 0 or key[0] >= len(self._data):
                raise IndexError("Row index out of range")

            if key[1] not in self._columns:
                raise KeyError(f"Column '{key[1]}' not found")

            self._data[key[0]][self._columns.index(key[1])] = value
            return

        # Set by column name
        if isinstance(key, str):
            if not isinstance(value, list) or not all(isinstance(item, QvdValue) for item in value):
                raise ValueError("Value must be a list of QVD values.")

            if len(value) != len(self._data):
                raise ValueError("Value must have the same number of elements as the table.")

            # Add a new column if it does not exist
            if key not in self._columns:
                self._columns.append(key)
                self._data = [row + [value[index]] for index, row in enumerate(self._data)]
                return

            column_index = self._columns.index(key)
            for row_index, row in enumerate(self._data):
                row[column_index] = value[row_index]

            return

        # Set by row index
        if isinstance(key, int):
            if key < 0 or key >= len(self._data):
                raise IndexError("Row index out of range")

            if not isinstance(value, list) or not all(isinstance(item, QvdValue) for item in value):
                raise ValueError("Value must be a list of QVD values.")

            if len(value) != len(self._columns):
                raise ValueError("Value must have the same number of elements as the table has columns.")

            self._data[key] = value
            return

        # Set by slice
        if isinstance(key, slice):
            is_valid_scalar = isinstance(value, QvdValue)

            is_valid_vector = (isinstance(value, list) and
                               all(isinstance(item, QvdValue) for item in value))

            is_valid_matrix = (isinstance(value, list) and
                               all(isinstance(sublist, list) and
                                   all(isinstance(item, QvdValue) for item in sublist) for sublist in value))

            if not is_valid_scalar and not is_valid_vector and not is_valid_matrix:
                raise ValueError("Value must be a valid scalar, vector, or matrix of QVD values.")

            # Replace all values in the slice with the same value
            if is_valid_scalar:
                for row in self._data[key]:
                    for index, _ in enumerate(row):
                        row[index] = value

                return

            # Replace all selected rows with the given vector
            if is_valid_vector:
                if len(value) != len(self._data[key]):
                    raise ValueError("Value must have the same number of elements as the table has columns.")

                for row in self._data[key]:
                    for index, _ in enumerate(row):
                        row[index] = value[index]

                return

            # Replace all selected rows and columns with the given matrix
            if is_valid_matrix:
                if len(value) != len(self._data[key]):
                    raise ValueError("Value must have the same number of elements as the slice has rows.")

                for row_index, row in enumerate(self._data[key]):
                    if len(value[row_index]) != len(row):
                        raise ValueError("Value must have the same number of elements as the table has columns.")

                    for index, _ in enumerate(row):
                        row[index] = value[row_index][index]

                return

        raise TypeError("Key must be a supported/valid one.")

    # pylint: disable-next=line-too-long
    def get(self, key: Union[str, int, slice, Tuple[int, str]]) -> Union[QvdValue, List[QvdValue], List[List[QvdValue]]]:
        """
        Returns the values for the specified key. As a shorthand, you can also use the indexing
        operator to get values.

        :param key: The key to retrieve.
        :return: The values for the specified key.

        Examples
        --------
        You can pass a single integer to get a row at the specified index:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.get(0) # Alias tbl[0]
            [1, 2, 3]
        
        You can pass a single string to get a column with the specified name:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.get("A") # Alias tbl["A"]
            [1, 4, 7]
        
        You can pass a tuple with an integer and a string to get a value at the specified row and column:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.get((0, "A")) # Alias tbl[0, "A"]
            1
        
        You can pass a slice to get a subset of the data table:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.get(slice(0, 2)) # Alias tbl[0:2]
            [[1, 2, 3], [4, 5, 6]]
        """
        # Access by row and column index
        if isinstance(key, tuple):
            if not isinstance(key[0], int):
                raise TypeError("Row must be a valid row index.")

            if not isinstance(key[1], str):
                raise TypeError("Column must be a valid column name.")

            if key[0] < 0 or key[0] >= len(self._data):
                raise IndexError("Row index out of range")

            if key[1] not in self._columns:
                raise KeyError(f"Column '{key[1]}' not found")

            return self._data[key[0]][self._columns.index(key[1])]

        # Access by column name
        if isinstance(key, str):
            if key not in self._columns:
                raise KeyError(f"Column '{key}' not found")

            column_index = self._columns.index(key)
            return [row[column_index] for row in self._data]

        # Access by row index
        if isinstance(key, int):
            if key < 0 or key >= len(self._data):
                raise IndexError("Row index out of range")

            return self._data[key]

        # Access by slice
        if isinstance(key, slice):
            return self._data[key]

        raise TypeError("Key must be a supported/valid one.")

    def append(self, row: List[QvdValue]) -> None:
        """
        Appends a new row to the data table.

        :param row: The row to append.
        """
        if len(row) != len(self._columns):
            raise ValueError("Row must have the same number of elements as the table has columns.")

        self._data.append(row)

    def insert(self, index: int, row: List[QvdValue]) -> None:
        """
        Inserts a new row at the specified index.

        :param index: The index to insert the row.
        :param row: The row to insert.
        """
        if len(row) != len(self._columns):
            raise ValueError("Row must have the same number of elements as the table has columns.")

        if index < 0 or index > len(self._data):
            raise IndexError("Index out of range")

        self._data.insert(index, row)

    def drop(self, key: Union[int, str, List[int], List[str]], axis: Literal["rows", "columns"] = "rows") -> None:
        """
        Drops the specified rows or columns from the data table.

        :param key: The key to drop.
        :param axis: The axis to drop along. Must be either 'rows' or 'columns'.

        Examples
        --------
        You can drop a single row by passing an integer:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.drop(1)
            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            7    8    9
        
        You can drop multiple rows by passing a list of integers:
        
            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.drop([0, 2])
            >>> tbl
            A    B    C
            ---  ---  ---
            4    5    6
        
        You can drop a single column by passing a string:
        
            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.drop("B", axis="columns")
            >>> tbl
            A    C
            ---  ---
            1    3
            4    6
        
        You can drop multiple columns by passing a list of strings:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.drop(["A", "C"], axis="columns")
            >>> tbl
            B
            ---
            2
            5
            8
        """
        if axis == "rows":
            if isinstance(key, int):
                if key < 0 or key >= len(self._data):
                    raise IndexError("Row index out of range")

                del self._data[key]
            elif isinstance(key, list):
                for index in key:
                    if index < 0 or index >= len(self._data):
                        raise IndexError("Row index out of range")

                for index in sorted(key, reverse=True):
                    del self._data[index]
            else:
                raise TypeError("Key must be a valid row index or a list of row indices.")
        elif axis == "columns":
            if isinstance(key, str):
                if key not in self._columns:
                    raise KeyError(f"Column '{key}' not found")

                column_index = self._columns.index(key)
                for row in self._data:
                    del row[column_index]

                self._columns.remove(key)
            elif isinstance(key, list):
                for column in key:
                    if column not in self._columns:
                        raise KeyError(f"Column '{column}' not found")

                for column in sorted(key, reverse=True):
                    column_index = self._columns.index(column)
                    for row in self._data:
                        del row[column_index]

                    self._columns.remove(column)
            else:
                raise TypeError("Key must be a valid column name or a list of column names.")
        else:
            raise ValueError("Axis must be either 'rows' or 'columns'.")

    # pylint: disable-next=line-too-long
    def __getitem__(self, key: Union[str, int, slice, Tuple[int, str]]) -> Union[QvdValue, List[QvdValue], List[List[QvdValue]]]:
        """
        Returns the values for the specified key. It is a shorthand for the get method.

        :param key: The key to retrieve.
        :return: The values for the specified key.
        """
        return self.get(key)

    # pylint: disable-next=line-too-long
    def __setitem__(self, key: Union[str, int, slice, Tuple[int, str]], value: Union[QvdValue, List[QvdValue], List[List[QvdValue]]]) -> None:
        """
        Sets the value for the specified key. It is a shorthand for the set method.

        :param key: The key to set.
        :param value: The value to set.
        """
        self.set(key, value)

    def __str__(self) -> str:
        """
        Returns a string representation of the data table.

        :return: The string representation.
        """
        return tabulate(self._data, headers=self._columns)

    def __repr__(self) -> str:
        """
        Returns a string representation of the data table.

        :return: The string representation.
        """
        return self.__str__()

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
        Persists the data table to a QVD file.

        :param path: The path to the QVD file.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.writer import QvdFileWriter

        QvdFileWriter(path, self).write()

    def to_stream(self, target: BinaryIO):
        """
        Writes the QVD file to a binary stream.

        :param target: The binary stream to write to.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.writer import QvdFileWriter

        QvdFileWriter(target, self).write()

    def to_dict(self) -> Dict[str, any]:
        """
        Converts the data table to a dictionary.

        :return: The dictionary representation of the data table.

        Examples
        --------
        You can convert the data table to a dictionary:

            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
            >>> tbl.to_dict()
            {'columns': ['A', 'B', 'C'], 'data': [[1, 2, 3], [4, 5, 6], [7, 8, 9]}
        """
        return {"columns": self._columns, "data": [[value.display_value for value in row] for row in self._data]}

    def to_pandas(self) -> "pd.DataFrame":
        """
        Converts the data table to a pandas data table. For value conversion, the calculation value
        is used.

        .. important::

            This method requires the pandas library to be installed. See `pandas`_ for more information.

        :return: The pandas data table.

        .. _pandas: https://pandas.pydata.org/
        """
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "Pandas is not installed. Please install it using `pip install pandas`."
            ) from exc

        return pd.DataFrame([[value.calculation_value for value in row] for row in self._data], columns=self._columns)

    @staticmethod
    def from_qvd(path: str) -> "QvdTable":
        """
        Loads a QVD file and returns its data table.

        :param path: The path to the QVD file.
        :return: The data table of the QVD file.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.reader import QvdFileReader

        return QvdFileReader(path).read()

    @staticmethod
    def from_stream(source: BinaryIO) -> "QvdTable":
        """
        Constructs a new QVD data table from a binary stream.

        :param source: The source to the QVD file.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.reader import QvdFileReader

        return QvdFileReader(source).read()

    @staticmethod
    def from_dict(data: Dict[str, any]) -> "QvdTable":
        """
        Constructs a new QVD data table from a raw value dictionary.

        :param data: The dictionary representation of the data table.
        :return: The QVD data table.

        Examples
        --------
        You can construct a data table from a dictionary:

            >>> tbl = QvdTable.from_dict({
            ...     "columns": ["A", "B", "C"],
            ...     "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            ... })
            >>> tbl
            A    B    C
            ---  ---  ---
            1    2    3
            4    5    6
            7    8    9
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
        Constructs a new QVD data table from a pandas data frame.

        .. important::

            This method requires the pandas library to be installed. See `pandas`_ for more information.

        :param df: The pandas data frame.
        :return: The QVD data table.

        .. _pandas: https://pandas.pydata.org/
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
