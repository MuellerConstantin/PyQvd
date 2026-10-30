"""
Module contains the :class:`QvdTable` class, which represents the internal data table of a QVD file.
"""

from copy import deepcopy
import datetime as dt
from decimal import Decimal
from functools import cmp_to_key
from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple, BinaryIO, Dict, Union, Literal, Callable, Optional
from tabulate import tabulate
from pyqvd.qvd.values import QvdValue, IntegerValue, DoubleValue, StringValue, DualDoubleValue
from pyqvd.qvd.logical import TimeValue, DateValue, TimestampValue, IntervalValue, MoneyValue

if TYPE_CHECKING:
    import pandas as pd
    from pyqvd.io import QvdFileWriterOptions

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
        # Ensure the number of columns matches the number of values in each record
        if len(data) > 0 and len(data[0]) != len(columns):
            raise ValueError("The number of columns must match the number of values in each record.")

        # Ensure all column names are unique
        if len(set(columns)) != len(columns):
            raise ValueError("All column names must be unique.")

        # Ensure all column names are strings
        if not all(isinstance(column, str) for column in columns):
            raise TypeError("All column names must be strings.")

        self._data: List[List[QvdValue]] = data
        self._columns: List[str] = columns

    @property
    def data(self) -> List[List[QvdValue]]:
        """
        Returns the internally stored data. This property is read-only and immutable.

        :return: The data.
        """
        return deepcopy(self._data)

    @property
    def columns(self) -> List[str]:
        """
        Returns the columns of the data table. This property is read-only and immutable.

        :return: The column names.
        """
        return deepcopy(self._columns)

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

    def rename(self, columns: Dict[str, str]) -> "QvdTable":
        """
        Renames the columns of the data table.

        :param columns: A dictionary mapping the old column names to the new column names.
        :return: The data table with the renamed columns.
        """
        new_columns = [columns.get(column, column) for column in self._columns]
        return QvdTable(self._data, new_columns)

    def head(self, n: int = 5) -> "QvdTable":
        """
        Returns the first n rows of the data table.

        :param n: The number of rows to return.
        :return: The first n rows.
        """
        return QvdTable(self._data[:n], self._columns)

    def tail(self, n: int = 5) -> "QvdTable":
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

    def copy(self, deep: bool = True) -> "QvdTable":
        """
        Returns a copy of the data table.

        :param deep: Whether to perform a deep copy.
        :return: The copy of the data table.
        """
        if deep:
            return deepcopy(self)
        return QvdTable(self._data, self._columns)

    # pylint: disable-next=line-too-long
    def set(self, key: Union[str, int, slice, Tuple[int, str]], value: Union[any, List[any], List[List[any]]]) -> None:
        """
        Sets the value for the specified key. As a shorthand, you can also use the indexing
        operator to set values.
        
        It is possible to set single values, add columns, and overwrite rows or columns
        with a list of values. Values can also be native Python types, which are automatically
        converted to QvdValue objects.

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
            if not isinstance(key[0], int):
                raise TypeError("Row must be a valid row index.")

            if not isinstance(key[1], str):
                raise TypeError("Column must be a valid column name.")

            if key[0] < 0 or key[0] >= len(self._data):
                raise IndexError("Row index out of range")

            if key[1] not in self._columns:
                raise KeyError(f"Column '{key[1]}' not found")

            value = value if isinstance(value, QvdValue) else QvdTable._get_symbol_from_value(value)

            self._data[key[0]][self._columns.index(key[1])] = value
            return

        # Set by column name
        if isinstance(key, str):
            if not isinstance(value, list):
                raise ValueError("Value must be a list of values.")

            if len(value) != len(self._data):
                raise ValueError("Value must have the same number of elements as the table.")

            # Add a new column if it does not exist
            if key not in self._columns:
                self._columns.append(key)
                self._data = [row + [value[index] if isinstance(value[index], QvdValue) else
                                     QvdTable._get_symbol_from_value(value[index])]
                                     for index, row in enumerate(self._data)]
                return

            value = [value if isinstance(value, QvdValue) else QvdTable._get_symbol_from_value(value)
                     for value in value]

            column_index = self._columns.index(key)
            for row_index, row in enumerate(self._data):
                row[column_index] = value[row_index]

            return

        # Set by row index
        if isinstance(key, int):
            if key < 0 or key >= len(self._data):
                raise IndexError("Row index out of range")

            if not isinstance(value, list):
                raise ValueError("Value must be a list of values.")

            if len(value) != len(self._columns):
                raise ValueError("Value must have the same number of elements as the table has columns.")

            value = [value if isinstance(value, QvdValue) else QvdTable._get_symbol_from_value(value)
                     for value in value]

            self._data[key] = value
            return

        # Set by slice
        if isinstance(key, slice):
            # Replace all selected rows and columns with the given matrix
            if isinstance(value, list) and all(isinstance(sublist, list) for sublist in value):
                if len(value) != len(self._data[key]):
                    raise ValueError("Value must have the same number of elements as the slice has rows.")

                for row_index, row in enumerate(self._data[key]):
                    if len(value[row_index]) != len(row):
                        raise ValueError("Value must have the same number of elements as the table has columns.")

                    for index, _ in enumerate(row):
                        row[index] = (value[row_index][index] if isinstance(value[row_index][index], QvdValue) else
                                      QvdTable._get_symbol_from_value(value[row_index][index]))

                return

            # Replace all selected rows with the given vector
            if isinstance(value, list):
                if len(value) != len(self._data[key]):
                    raise ValueError("Value must have the same number of elements as the table has columns.")

                for row in self._data[key]:
                    for index, _ in enumerate(row):
                        row[index] = (value[index] if isinstance(value[index], QvdValue) else
                                      QvdTable._get_symbol_from_value(value[index]))

                return

            for row in self._data[key]:
                for index, _ in enumerate(row):
                    row[index] = (value if isinstance(value, QvdValue) else QvdTable._get_symbol_from_value(value))

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

    def append(self, row: List[any]) -> None:
        """
        Appends a new row to the data table.

        :param row: The row to append.
        """
        if len(row) != len(self._columns):
            raise ValueError("Row must have the same number of elements as the table has columns.")

        row = [value if isinstance(value, QvdValue) else QvdTable._get_symbol_from_value(value) for value in row]

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

        row = [value if isinstance(value, QvdValue) else QvdTable._get_symbol_from_value(value) for value in row]

        self._data.insert(index, row)

    def drop(self, key: Union[int, str, List[int], List[str]], axis: Literal["rows", "columns"] = "rows",
             inplace: bool = False) -> 'QvdTable':
        """
        Drops the specified rows or columns from the data table.

        :param key: The key to drop.
        :param axis: The axis to drop along. Must be either 'rows' or 'columns'.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The data table with the specified rows or columns dropped.

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
            new_data = self._data if inplace else deepcopy(self._data)

            if isinstance(key, int):
                if key < 0 or key >= len(self._data):
                    raise IndexError("Row index out of range")

                del new_data[key]
            elif isinstance(key, list):
                for index in key:
                    if index < 0 or index >= len(self._data):
                        raise IndexError("Row index out of range")

                for index in sorted(key, reverse=True):
                    del new_data[index]
            else:
                raise TypeError("Key must be a valid row index or a list of row indices.")

            if inplace:
                self._data = new_data
                return self
            return QvdTable(new_data, deepcopy(self._columns))
        if axis == "columns":
            new_data = self._data if inplace else deepcopy(self._data)
            new_columns = self._columns if inplace else deepcopy(self._columns)

            if isinstance(key, str):
                if key not in new_columns:
                    raise KeyError(f"Column '{key}' not found")

                column_index = new_columns.index(key)
                for row in new_data:
                    del row[column_index]

                new_columns.remove(key)
            elif isinstance(key, list):
                for column in key:
                    if column not in new_columns:
                        raise KeyError(f"Column '{column}' not found")

                for column in sorted(key, reverse=True):
                    column_index = new_columns.index(column)
                    for row in new_data:
                        del row[column_index]

                    new_columns.remove(column)
            else:
                raise TypeError("Key must be a valid column name or a list of column names.")

            if inplace:
                self._data = new_data
                self._columns = new_columns
                return self
            return QvdTable(new_data, new_columns)
        raise ValueError("Axis must be either 'rows' or 'columns'.")

    def filter_by(self, column: str, condition: Callable[[QvdValue], bool],
                  inplace: bool = False) -> "QvdTable":
        """
        Filters the data table by the specified column and condition. By default a new data table
        is constructed with the filtered data.

        :param column: The column to filter by.
        :param condition: The condition to filter by.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The filtered data table.
        """
        if column not in self._columns:
            raise KeyError(f"Column '{column}' not found")

        column_index = self._columns.index(column)
        new_data = self._data if inplace else deepcopy(self._data)
        new_data = [row for row in new_data if condition(row[column_index])]

        if inplace:
            self._data = new_data
            return self
        return QvdTable(new_data, deepcopy(self._columns))

    def sort_by(self, column: str, ascending: bool = True,
                comparator: Optional[Callable[[QvdValue, QvdValue], int]] = None,
                na_position: Literal["first", "last"] = "first",
                inplace: bool = False) -> "QvdTable":
        """
        Sorts the data table by the specified column. By default a new data table is constructed
        with the sorted data.

        :param column: The column to sort by.
        :param ascending: Whether to sort in ascending
        :param comparator: The comparator function to use for sorting.
        :param na_position: Where to place missing values in the sorted data.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The sorted data table.
        """
        if column not in self._columns:
            raise KeyError(f"Column '{column}' not found")

        column_index = self._columns.index(column)
        new_data = self._data if inplace else deepcopy(self._data)
        new_data = [row for row in new_data if row[column_index] is not None]
        na_data = [row for row in new_data if row[column_index] is None]

        def _default_comparator(a: QvdValue, b: QvdValue) -> int:
            if a < b:
                return -1
            if a > b:
                return 1

            return 0

        if comparator is None:
            comparator = _default_comparator

        new_data.sort(key=cmp_to_key(lambda row1, row2: comparator(row1[column_index], row2[column_index])),
                      reverse=not ascending)

        if na_position == "first":
            new_data = na_data + new_data
        else:
            new_data = new_data + na_data

        if inplace:
            self._data = new_data
            return self
        return QvdTable(new_data, deepcopy(self._columns))

    def concat(self, *args: "QvdTable", inplace: bool = False) -> "QvdTable":
        """
        Concatenates multiple data tables into a single data table. The data tables are concatenated
        row-wise. If a column is missing in a data table, the values for its rows are filled with None
        and the column is added to the concatenated data table.

        .. important::

            Internally, this method uses the `copy.deepcopy` function to create a deep copy of the
            current data table and the data tables to concatenate. This can be very slow for large
            data tables with many concatenations. For better performance, consider using the `inplace`
            parameter to modify the current data table instead of returning a new data table. This
            will avoid the overhead of creating deep copies of the current data table.

        :param tables: The data tables to concatenate.
        :param inplace: Instead of returning a new data table, modify the current data table. This may
                        be faster for large data tables with many concatenations.
        :return: The concatenated data table.
        """
        if len(args) == 0:
            raise ValueError("At least one data table must be provided.")

        new_columns = deepcopy(self._columns)
        new_columns.extend(column for table in args for column in deepcopy(table.columns))
        new_columns = list(dict.fromkeys(new_columns).keys())

        # Because 'dict.fromkeys(...).keys()' is guaranteed to preserve the order of the keys,
        # we know for sure that the first columns are the ones from the current table. So we can
        # just add the data from the current table and add possible new columns from the other
        # tables to each current table's record.
        #
        # See: https://docs.python.org/3.7/whatsnew/3.7.html

        new_data = self._data if inplace else deepcopy(self._data)

        # Checks whether the tables to be appended have introduced new columns
        if len(new_columns) > len(self._columns):
            for row in new_data:
                row.extend([None] * (len(new_columns) - len(row)))

        for table in args:
            for row in table.data:
                new_row = [None] * len(new_columns)

                for index, column in enumerate(table.columns):
                    new_row[new_columns.index(column)] = deepcopy(row[index])

                new_data.append(new_row)

        if inplace:
            self._data = new_data
            self._columns = new_columns
            return self
        return QvdTable(new_data, new_columns)

    def join(self, other: "QvdTable", on: Union[str, List[str]],
             how: Literal["inner", "left", "right", "outer"] = "outer",
             lsuffix: Optional[str] = None, rsuffix: Optional[str] = None,
             inplace: bool = False) -> "QvdTable":
        """
        Joins the data table with another data table. By default a new data table is constructed
        with the joined data.

        :param other: The other data table to join with.
        :param on: The column(s) to join on.
        :param how: The type of join to perform.
        :param lsuffix: The suffix to append to overlapping column names from the left table.
        :param rsuffix: The suffix to append to overlapping column names from the right table.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The joined data table.

        Examples
        --------
        You can perform an inner join between two data tables:

            >>> tbl1
            A    B
            ---  ---
            1    2
            3    4
            5    6
            >>> tbl2
            A    C
            ---  ---
            1    7
            3    8
            7    9
            >>> tbl1.join(tbl2, on="A", how="inner")
            A    B    C
            ---  ---  ---
            1    2    7
            3    4    8
        
        You can use also suffixed for overlapping column names:

            >>> tbl1
            A    B
            ---  ---
            1    2
            3    4
            5    6
            >>> tbl2
            A    B
            ---  ---
            1    7
            3    8
            7    9
            >>> tbl1.join(tbl2, on="A", how="inner", lsuffix="_left", rsuffix="_right")
            A    B_left    B_right
            ---  ---       ---
            1    2         7
            3    4         8
        """
        if not isinstance(other, QvdTable):
            raise TypeError("Other must be a QVD table.")

        if isinstance(on, str):
            on = [on]

        if not all(column in self._columns for column in on):
            raise KeyError("Column(s) to join on must be present in the current table.")

        if not all(column in other.columns for column in on):
            raise KeyError("Column(s) to join on must be present in the other table.")

        if (any(column in self._columns for column in other.columns if column not in on) and
            (lsuffix is None and rsuffix is None)):
            raise ValueError("Ambiguous column name(s) found. Please specify a suffix for the columns.")

        if how == "inner":
            return self._inner_join(other, on, lsuffix, rsuffix, inplace)
        if how == "left":
            return self._left_join(other, on, lsuffix, rsuffix, inplace)
        if how == "right":
            return self._right_join(other, on, lsuffix, rsuffix, inplace)
        if how == "outer":
            return self._outer_join(other, on, lsuffix, rsuffix, inplace)
        raise ValueError("Invalid join type. Must be one of 'inner', 'left', 'right', or 'outer'.")

    def _left_join(self, other: "QvdTable", on: List[str], lsuffix: Optional[str] = None,
                   rsuffix: Optional[str] = None, inplace: bool = False) -> "QvdTable":
        """
        Performs a left join between the data table and another data table.

        :param other: The other data table to join with.
        :param on: The column(s) to join on.
        :param lsuffix: The suffix to append to overlapping column names from the left table.
        :param rsuffix: The suffix to append to overlapping column names from the right table.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The joined data table.
        """
        joined_columns = deepcopy(on)

        if lsuffix:
            joined_columns.extend(f"{column}{lsuffix}" for column in self.columns if column not in on)
        else:
            joined_columns.extend(column for column in self.columns if column not in on)

        if rsuffix:
            joined_columns.extend(f"{column}{rsuffix}" for column in other.columns if column not in on)
        else:
            joined_columns.extend(column for column in other.columns if column not in on)

        joined_columns = list(dict.fromkeys(joined_columns).keys())
        joined_data = []

        left_dict = {tuple(row[self._columns.index(key)] for key in on): row for row in self.data}
        right_dict = {tuple(row[other.columns.index(key)] for key in on): row for row in other.data}

        for key in left_dict.keys():
            if key in right_dict:
                joined_data.append(
                    deepcopy(list(key) +
                                [left_dict[key][self._columns.index(column)]
                                for column in self.columns if column not in on] +
                                [right_dict[key][other.columns.index(column)]
                                for column in other.columns if column not in on]))
            else:
                joined_data.append(
                    deepcopy(list(key) +
                                [left_dict[key][self._columns.index(column)]
                                for column in self.columns if column not in on] +
                                [None] * (len(other.columns) - len(on))))

        if inplace:
            self._data = joined_data
            self._columns = joined_columns
            return self
        return QvdTable(joined_data, joined_columns)

    def _right_join(self, other: "QvdTable", on: List[str], lsuffix: Optional[str] = None,
                   rsuffix: Optional[str] = None, inplace: bool = False) -> "QvdTable":
        """
        Performs a right join between the data table and another data table.

        :param other: The other data table to join with.
        :param on: The column(s) to join on.
        :param lsuffix: The suffix to append to overlapping column names from the left table.
        :param rsuffix: The suffix to append to overlapping column names from the right table.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The joined data table.
        """
        joined_columns = deepcopy(on)

        if rsuffix:
            joined_columns.extend(f"{column}{rsuffix}" for column in other.columns if column not in on)
        else:
            joined_columns.extend(column for column in other.columns if column not in on)

        if lsuffix:
            joined_columns.extend(f"{column}{lsuffix}" for column in self.columns if column not in on)
        else:
            joined_columns.extend(column for column in self.columns if column not in on)

        joined_columns = list(dict.fromkeys(joined_columns).keys())
        joined_data = []

        left_dict = {tuple(row[self._columns.index(key)] for key in on): row for row in self.data}
        right_dict = {tuple(row[other.columns.index(key)] for key in on): row for row in other.data}

        for key in right_dict.keys():
            if key in left_dict:
                joined_data.append(
                    deepcopy(list(key) +
                                [right_dict[key][self._columns.index(column)]
                                for column in self.columns if column not in on] +
                                [left_dict[key][other.columns.index(column)]
                                for column in other.columns if column not in on]))
            else:
                joined_data.append(
                    deepcopy(list(key) +
                                [right_dict[key][other.columns.index(column)]
                                for column in other.columns if column not in on] +
                                [None] * (len(self.columns) - len(on))))

        if inplace:
            self._data = joined_data
            self._columns = joined_columns
            return self
        return QvdTable(joined_data, joined_columns)

    def _outer_join(self, other: "QvdTable", on: List[str], lsuffix: Optional[str] = None,
                   rsuffix: Optional[str] = None, inplace: bool = False) -> "QvdTable":
        """
        Performs an outer join between the data table and another data table.

        :param other: The other data table to join with.
        :param on: The column(s) to join on.
        :param lsuffix: The suffix to append to overlapping column names from the left table.
        :param rsuffix: The suffix to append to overlapping column names from the right table.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The joined data table.
        """
        joined_columns = deepcopy(on)

        if lsuffix:
            joined_columns.extend(f"{column}{lsuffix}" for column in self.columns if column not in on)
        else:
            joined_columns.extend(column for column in self.columns if column not in on)

        if rsuffix:
            joined_columns.extend(f"{column}{rsuffix}" for column in other.columns if column not in on)
        else:
            joined_columns.extend(column for column in other.columns if column not in on)

        joined_columns = list(dict.fromkeys(joined_columns).keys())
        joined_data = []

        left_dict = {tuple(row[self._columns.index(key)] for key in on): row for row in self.data}
        right_dict = {tuple(row[other.columns.index(key)] for key in on): row for row in other.data}

        for key in left_dict.keys():
            if key in right_dict:
                joined_data.append(
                    deepcopy(list(key) +
                                [left_dict[key][self._columns.index(column)]
                                for column in self.columns if column not in on] +
                                [right_dict[key][other.columns.index(column)]
                                for column in other.columns if column not in on]))
            else:
                joined_data.append(
                    deepcopy(list(key) +
                                [left_dict[key][self._columns.index(column)]
                                for column in self.columns if column not in on] +
                                [None] * (len(other.columns) - len(on))))

        for key in right_dict.keys():
            if key not in left_dict:
                joined_data.append(
                    deepcopy(list(key) +
                                [None] * (len(self.columns) - len(on)) +
                                [right_dict[key][other.columns.index(column)]
                                for column in other.columns if column not in on]))

        if inplace:
            self._data = joined_data
            self._columns = joined_columns
            return self
        return QvdTable(joined_data, joined_columns)

    def _inner_join(self, other: "QvdTable", on: List[str], lsuffix: Optional[str] = None,
                   rsuffix: Optional[str] = None, inplace: bool = False) -> "QvdTable":
        """
        Performs an inner join between the data table and another data table.

        :param other: The other data table to join with.
        :param on: The column(s) to join on.
        :param lsuffix: The suffix to append to overlapping column names from the left table.
        :param rsuffix: The suffix to append to overlapping column names from the right table.
        :param inplace: Instead of returning a new data table, modify the current data table.
        :return: The joined data table.
        """
        joined_columns = deepcopy(on)

        if lsuffix:
            joined_columns.extend(f"{column}{lsuffix}" for column in self.columns if column not in on)
        else:
            joined_columns.extend(column for column in self.columns if column not in on)

        if rsuffix:
            joined_columns.extend(f"{column}{rsuffix}" for column in other.columns if column not in on)
        else:
            joined_columns.extend(column for column in other.columns if column not in on)

        joined_columns = list(dict.fromkeys(joined_columns).keys())
        joined_data = []

        left_dict = {tuple(row[self._columns.index(key)] for key in on): row for row in self.data}
        right_dict = {tuple(row[other.columns.index(key)] for key in on): row for row in other.data}

        for key in left_dict.keys():
            if key in right_dict:
                joined_data.append(
                    deepcopy(list(key) +
                                [left_dict[key][self._columns.index(column)]
                                for column in self.columns if column not in on] +
                                [right_dict[key][other.columns.index(column)]
                                for column in other.columns if column not in on]))

        if inplace:
            self._data = joined_data
            self._columns = joined_columns
            return self
        return QvdTable(joined_data, joined_columns)

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

    def to_qvd(self, path: Union[str, Path], options: "QvdFileWriterOptions" = None):
        """
        Persists the data table to a QVD file.

        :param path: The path to the QVD file (str or Path object).
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.writer import QvdFileWriter

        QvdFileWriter(path, self, options).write()

    def to_stream(self, target: BinaryIO, options: "QvdFileWriterOptions" = None):
        """
        Writes the QVD file to a binary stream.

        :param target: The binary stream to write to.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.writer import QvdFileWriter

        QvdFileWriter(target, self, options).write()

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
        data = [[QvdTable._get_value_from_symbol(symbol) for symbol in row] for row in self._data]
        return {"columns": self._columns, "data": data}

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

        convert = QvdTable._get_value_from_symbol
        data = {}

        # Cells with the same value share one QvdValue instance, which the table keeps alive, so
        # its id identifies it. In columns with many repeated values, each distinct instance is
        # converted only once, saving the costly conversion of dates and times. Columns with mostly
        # distinct values are converted directly, as deduplicating them costs more than it saves.
        for column, values in zip(self._columns, zip(*self._data)):
            ids = list(map(id, values))
            distinct = dict(zip(ids, values))

            if len(distinct) * 2 > len(values):
                data[column] = list(map(convert, values))
            else:
                converted = {key: convert(value) for key, value in distinct.items()}
                data[column] = list(map(converted.__getitem__, ids))

        return pd.DataFrame(data, columns=self._columns)

    @staticmethod
    def from_qvd(path: Union[str, Path], chunk_size: int = None) -> Union["QvdTable", Iterator["QvdTable"]]:
        """
        Loads a QVD file and returns its data table.

        :param path: The path to the QVD file (str or Path object).
        :param chunk_size: Optional chunk size, as number of records, to read the QVD file in chunks.
        :return: The data table of the QVD file or an iterator over the slices of the data table.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.reader import QvdFileReader

        return QvdFileReader(path, chunk_size).read()

    @staticmethod
    def from_stream(source: BinaryIO, chunk_size: int = None) -> Union["QvdTable", Iterator["QvdTable"]]:
        """
        Constructs a new QVD data table from a binary stream.

        :param source: The source to the QVD file.
        :param chunk_size: Optional chunk size, as number of records, to read the QVD file in chunks.
        :return: The data table of the QVD file or an iterator over the slices of the data table.
        """
        # pylint: disable=import-outside-toplevel
        from pyqvd.io.reader import QvdFileReader

        return QvdFileReader(source, chunk_size).read()

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
        table_data = [[QvdTable._get_symbol_from_value(value) for value in row] for row in data["data"]]
        return QvdTable(table_data, data["columns"])

    @staticmethod
    def from_pandas(df: "pd.DataFrame", vectorized=True) -> "QvdTable":
        """
        Constructs a new QVD data table from a pandas data frame.

        .. important::

            This method requires the pandas library to be installed. See `pandas`_ for more information.

        :param df: The pandas data frame.
        :param vectorized: Optional flag to enable vectorized conversion.
        :return: The QVD data table.

        .. _pandas: https://pandas.pydata.org/
        """
        try:
            # pylint: disable=import-outside-toplevel
            import pandas as pd
            from pandas.api.types import is_integer_dtype, is_float_dtype, is_datetime64_any_dtype, is_timedelta64_dtype
            import numpy as np
        except ImportError as exc:
            raise ImportError(
                "Pandas is not installed. Please install it using `pip install pandas`."
            ) from exc

        def is_int32(value: int) -> bool:
            try:
                np.int32(value)
                return True
            except OverflowError:
                return False

        def _get_symbol_from_pandas_value(value: any) -> QvdValue:
            if value is None or pd.isna(value):
                return None

            value_type = type(value)

            if is_integer_dtype(value_type):
                if is_int32(int(value)):
                    return IntegerValue(int(value))
                return DualDoubleValue(float(value), str(value))
            if is_float_dtype(value_type):
                return DoubleValue(float(value))
            if isinstance(value, pd.Timestamp):
                return TimestampValue.from_timestamp(value.to_pydatetime())
            if is_datetime64_any_dtype(value_type):
                return TimestampValue.from_timestamp(pd.Timestamp(value).to_pydatetime())
            if isinstance(value, pd.Timedelta):
                return IntervalValue.from_interval(value.to_pytimedelta())

            return QvdTable._get_symbol_from_value(value)

        def _get_symbol_from_pandas_value_(column):

            value_type = column.dtype

            if is_integer_dtype(value_type):
                val_max = int(column.abs().max())
                if is_int32(val_max):
                    return column.apply(lambda x: IntegerValue(int(x)) if not pd.isna(x) else None)
                return column.apply(lambda x: DualDoubleValue(float(x), str(x)) if not pd.isna(x) else None)
            if is_float_dtype(value_type):
                return column.apply(lambda x: DoubleValue(float(x)) if not pd.isna(x) else None)
            if is_datetime64_any_dtype(value_type):
                return column.apply(lambda x: TimestampValue.from_timestamp(x.to_pydatetime())
                                    if not pd.isna(x) else None)
            if is_timedelta64_dtype(value_type):
                return column.apply(lambda x: IntervalValue.from_interval(x.to_pytimedelta())
                                    if not pd.isna(x) else None)

            return column.apply(lambda x: QvdTable._get_symbol_from_value(x) if not pd.isna(x) else None)

        if not vectorized:
            data = [[_get_symbol_from_pandas_value(value) for value in row] for row in df.values]
        else:
            data = df.apply(_get_symbol_from_pandas_value_).values.tolist()
        return QvdTable(data, df.columns.tolist())

    @staticmethod
    def _get_symbol_from_value(value: any) -> QvdValue:
        """
        Converts a raw python value to a QVD value.

        :param value: The value to convert.
        :return: The QVD value.
        """
        if value is None:
            return None

        if isinstance(value, QvdValue):
            return value

        if isinstance(value, int):
            return IntegerValue(value)
        if isinstance(value, float):
            return DoubleValue(value)
        if isinstance(value, Decimal):
            return MoneyValue.from_money(value)
        if isinstance(value, dt.time):
            return TimeValue.from_time(value)
        if isinstance(value, dt.datetime):
            return TimestampValue.from_timestamp(value)
        if isinstance(value, dt.date):
            return DateValue.from_date(value)
        if isinstance(value, dt.timedelta):
            return IntervalValue.from_interval(value)

        return StringValue(str(value))

    @staticmethod
    def _get_value_from_symbol(value: QvdValue) -> any:
        """
        Converts a QVD value to a raw python value.

        :param value: The value to convert.
        :return: The raw python value.
        """
        if value is None:
            return None

        if isinstance(value, TimeValue):
            return value.time
        if isinstance(value, DateValue):
            return value.date
        if isinstance(value, TimestampValue):
            return value.timestamp
        if isinstance(value, IntervalValue):
            return value.interval
        if isinstance(value, MoneyValue):
            return value.money

        return value.calculation_value
