"""
Tests the functionality related to reading files.
"""

from typing import TYPE_CHECKING
import pytest
from pyqvd import QvdTable, IntegerValue, StringValue

if TYPE_CHECKING:
    import pandas as pd

def test_qvd_value_comparison():
    """
    Tests the comparison of two QVD values.
    """
    x1 = IntegerValue(1)
    x2 = IntegerValue(1)
    x3 = IntegerValue(2)

    assert x1 < x3
    assert x1 <= x3
    assert x3 > x1
    assert x3 >= x1
    assert x1 == x2
    assert x1 <= x2
    assert x1 >= x2

def test_construct_qvd_table_from_dict():
    """
    Tests if a QVD table, constructed from a dictionary, can be read properly.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    assert tbl is not None
    assert tbl.shape is not None
    assert tbl.shape[0] == 5
    assert tbl.shape[1] == 2
    assert tbl.columns is not None
    assert len(tbl.columns) == 2
    assert tbl.data is not None
    assert len(tbl.data) == 5
    assert tbl.head(2).shape == (2, 2)
    assert tbl.to_dict() == raw_tbl

def test_construct_qvd_table_from_pandas_df():
    """
    Tests if a QVD table, constructed from a pandas DataFrame, can be read properly.
    """
    try:
        # pylint: disable=import-outside-toplevel
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "Pandas is not installed. Please install it using `pip install pandas`."
        ) from exc

    raw_df = pd.DataFrame({
        "Key": [1, 2, 3, 4, 5],
        "Value": ["A", "B", "C", "D", "E"]
    })

    tbl = QvdTable.from_pandas(raw_df)

    assert tbl is not None
    assert tbl.shape is not None
    assert tbl.shape[0] == 5
    assert tbl.shape[1] == 2
    assert tbl.columns is not None
    assert len(tbl.columns) == 2
    assert tbl.data is not None
    assert len(tbl.data) == 5
    assert tbl.head(2).shape == (2, 2)
    assert tbl.to_pandas().equals(raw_df)

def test_qvd_table_to_dict():
    """
    Tests if a QVD table can be converted to a dictionary properly.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    assert tbl.to_dict() == raw_tbl

def test_qvd_table_to_pandas():
    """
    Tests if a QVD table can be converted to a pandas DataFrame properly.
    """
    try:
        # pylint: disable=import-outside-toplevel
        import pandas as pd
    except ImportError as exc:
        raise ImportError(
            "Pandas is not installed. Please install it using `pip install pandas`."
        ) from exc

    raw_df = pd.DataFrame({
        "Key": [1, 2, 3, 4, 5],
        "Value": ["A", "B", "C", "D", "E"]
    })

    tbl = QvdTable.from_pandas(raw_df)

    assert tbl.to_pandas().equals(raw_df)

def test_construct_qvd_table_directly():
    """
    Tests if a QVD table can be constructed directly.
    """
    tbl = QvdTable(
        columns=["Key", "Value"],
        data=[
            [IntegerValue(1), StringValue("A")],
            [IntegerValue(2), StringValue("B")],
            [IntegerValue(3), StringValue("C")],
            [IntegerValue(4), StringValue("D")],
            [IntegerValue(5), StringValue("E")]
        ]
    )

    assert tbl is not None
    assert tbl.shape is not None
    assert tbl.shape[0] == 5
    assert tbl.shape[1] == 2
    assert tbl.columns is not None
    assert len(tbl.columns) == 2
    assert tbl.data is not None
    assert len(tbl.data) == 5
    assert tbl.head(2).shape == (2, 2)

def test_qvd_table_constuct_directly_with_invalid_shape():
    """
    Tests if constructing a QVD table directly with invalid data raises an exception.
    """
    with pytest.raises(Exception):
        QvdTable(
            columns=["Key", "Value"],
            data=[
                [IntegerValue(1), StringValue("A")],
                [IntegerValue(2)],
                [IntegerValue(3), StringValue("C")]
            ]
        )

def test_qvd_table_get_by_tuple():
    """
    Tests the functionality of getting a cell from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    value = tbl.get((0, "Key"))

    assert value is not None
    assert value.display_value == 1

def test_qvd_table_get_by_invalid_tuple():
    """
    Tests the functionality of getting an invalid cell from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(IndexError):
        tbl.get((5, "Key"))

def test_qvd_table_get_by_column():
    """
    Tests the functionality of getting a column from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    values = tbl.get("Key")

    assert values is not None
    assert len(values) == 5
    assert values[0].display_value == 1
    assert values[1].display_value == 2
    assert values[2].display_value == 3
    assert values[3].display_value == 4
    assert values[4].display_value == 5

def test_qvd_table_get_by_invalid_column():
    """
    Tests the functionality of getting an invalid column from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(KeyError):
        tbl.get("Invalid")

def test_qvd_table_get_by_row():
    """
    Tests the functionality of getting a row from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    values = tbl.get(0)

    assert values is not None
    assert len(values) == 2
    assert values[0].display_value == 1
    assert values[1].display_value == "A"

def test_qvd_table_get_by_invalid_row():
    """
    Tests the functionality of getting an invalid row from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(IndexError):
        tbl.get(5)

def test_qvd_table_get_by_slice():
    """
    Tests the functionality of getting a slice from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    values = tbl.get(slice(0, 2))

    assert values is not None
    assert len(values) == 2
    assert values[0][0].display_value == 1
    assert values[0][1].display_value == "A"
    assert values[1][0].display_value == 2
    assert values[1][1].display_value == "B"

def test_qvd_table_getitem_by_tuple():
    """
    Tests the functionality of getting a cell from a QVD table using the getitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    value = tbl[0, "Key"]

    assert value is not None
    assert value.display_value == 1

def test_qvd_table_getitem_by_column():
    """
    Tests the functionality of getting a column from a QVD table using the getitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    values = tbl["Key"]

    assert values is not None
    assert len(values) == 5
    assert values[0].display_value == 1
    assert values[1].display_value == 2
    assert values[2].display_value == 3
    assert values[3].display_value == 4
    assert values[4].display_value == 5

def test_qvd_table_getitem_by_row():
    """
    Tests the functionality of getting a row from a QVD table using the getitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    values = tbl[0]

    assert values is not None
    assert len(values) == 2
    assert values[0].display_value == 1
    assert values[1].display_value == "A"

def test_qvd_table_getitem_by_slice():
    """
    Tests the functionality of getting a slice from a QVD table using the getitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    values = tbl[0:2]

    assert values is not None
    assert len(values) == 2
    assert values[0][0].display_value == 1
    assert values[0][1].display_value == "A"
    assert values[1][0].display_value == 2
    assert values[1][1].display_value == "B"

def test_qvd_table_set_by_column():
    """
    Tests the functionality of setting a column in a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.set("Key", [IntegerValue(6), IntegerValue(7), IntegerValue(8), IntegerValue(9), IntegerValue(10)])

    assert tbl.at(0, "Key").display_value == 6
    assert tbl.at(1, "Key").display_value == 7
    assert tbl.at(2, "Key").display_value == 8
    assert tbl.at(3, "Key").display_value == 9
    assert tbl.at(4, "Key").display_value == 10

def test_qvd_table_add_column():
    """
    Tests the functionality of adding a column to a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.set("New", [IntegerValue(4), IntegerValue(5), IntegerValue(6)])

    assert tbl.shape == (3, 3)
    assert tbl.at(0, "New").display_value == 4
    assert tbl.at(1, "New").display_value == 5
    assert tbl.at(2, "New").display_value == 6

def test_qvd_table_set_by_column_with_invalid_shape():
    """
    Tests the functionality of setting a column in a QVD table with invalid data raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(ValueError):
        tbl.set("Key", [IntegerValue(6), IntegerValue(7), IntegerValue(8)])

def test_qvd_table_set_by_row():
    """
    Tests the functionality of setting a row in a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.set(0, [IntegerValue(6), StringValue("F")])

    assert tbl.at(0, "Key").display_value == 6
    assert tbl.at(0, "Value").display_value == "F"

def test_qvd_table_set_by_invalid_row():
    """
    Tests the functionality of setting an invalid row in a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(IndexError):
        tbl.set(5, [IntegerValue(6), StringValue("F")])

def test_qvd_table_set_by_row_with_invalid_shape():
    """
    Tests the functionality of setting a row in a QVD table with invalid data raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(ValueError):
        tbl.set(0, [IntegerValue(6)])

def test_qvd_table_set_by_slice():
    """
    Tests the functionality of setting a slice in a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    new_data = [
        [IntegerValue(6), StringValue("F")],
        [IntegerValue(7), StringValue("G")],
        [IntegerValue(8), StringValue("H")]
    ]

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.set(slice(1, 4), new_data)

    assert tbl.at(1, "Key").display_value == 6
    assert tbl.at(1, "Value").display_value == "F"
    assert tbl.at(2, "Key").display_value == 7
    assert tbl.at(2, "Value").display_value == "G"
    assert tbl.at(3, "Key").display_value == 8
    assert tbl.at(3, "Value").display_value == "H"

def test_qvd_table_set_by_slice_with_invalid_shape():
    """
    Tests the functionality of setting a slice in a QVD table with invalid data raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    new_data = [
        [IntegerValue(6), StringValue("F")],
        [IntegerValue(7), StringValue("G")]
    ]

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(ValueError):
        tbl.set(slice(1, 4), new_data)

def test_qvd_table_setitem_by_column():
    """
    Tests the functionality of setting a column in a QVD table using the setitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl["Key"] = [IntegerValue(6), IntegerValue(7), IntegerValue(8), IntegerValue(9), IntegerValue(10)]

    assert tbl.at(0, "Key").display_value == 6
    assert tbl.at(1, "Key").display_value == 7
    assert tbl.at(2, "Key").display_value == 8
    assert tbl.at(3, "Key").display_value == 9
    assert tbl.at(4, "Key").display_value == 10

def test_qvd_table_setitem_add_column():
    """
    Tests the functionality of adding a column to a QVD table using the setitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl["New"] = [IntegerValue(4), IntegerValue(5), IntegerValue(6)]

    assert tbl.shape == (3, 3)
    assert tbl.at(0, "New").display_value == 4
    assert tbl.at(1, "New").display_value == 5
    assert tbl.at(2, "New").display_value == 6

def test_qvd_table_setitem_by_row():
    """
    Tests the functionality of setting a row in a QVD table using the setitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl[0] = [IntegerValue(6), StringValue("F")]

    assert tbl.at(0, "Key").display_value == 6
    assert tbl.at(0, "Value").display_value == "F"

def test_qvd_table_setitem_by_slice():
    """
    Tests the functionality of setting a slice in a QVD table using the setitem method.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    new_data = [
        [IntegerValue(6), StringValue("F")],
        [IntegerValue(7), StringValue("G")],
        [IntegerValue(8), StringValue("H")]
    ]

    tbl = QvdTable.from_dict(raw_tbl)
    tbl[1:4] = new_data

    assert tbl.at(1, "Key").display_value == 6
    assert tbl.at(1, "Value").display_value == "F"
    assert tbl.at(2, "Key").display_value == 7
    assert tbl.at(2, "Value").display_value == "G"
    assert tbl.at(3, "Key").display_value == 8
    assert tbl.at(3, "Value").display_value == "H"

def test_qvd_table_append_row():
    """
    Tests the functionality of appending a row to a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.append([IntegerValue(2), StringValue("B")])

    assert tbl.shape == (2, 2)
    assert tbl.at(1, "Key").display_value == 2
    assert tbl.at(1, "Value").display_value == "B"

def test_qvd_table_append_row_with_invalid_shape():
    """
    Tests the functionality of appending a row to a QVD table with invalid data raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(ValueError):
        tbl.append([IntegerValue(2)])

def test_qvd_table_insert_row():
    """
    Tests the functionality of inserting a row to a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.insert(0, [IntegerValue(1), StringValue("A")])

    assert tbl.shape == (5, 2)
    assert tbl.at(0, "Key").display_value == 1
    assert tbl.at(0, "Value").display_value == "A"

def test_qvd_table_insert_row_with_invalid_shape():
    """
    Tests the functionality of inserting a row to a QVD table with invalid data raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(ValueError):
        tbl.insert(0, [IntegerValue(1)])

def test_qvd_table_insert_row_with_invalid_index():
    """
    Tests the functionality of inserting a row to a QVD table with an invalid index raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(IndexError):
        tbl.insert(5, [IntegerValue(1), StringValue("A")])

def test_qvd_table_drop_column():
    """
    Tests the functionality of dropping a column from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.drop("New", axis="columns")

    assert tbl.shape == (3, 2)
    assert tbl.columns == ["Key", "Value"]

def test_qvd_table_drop_column_with_invalid_name():
    """
    Tests the functionality of dropping an invalid column from a QVD table raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(KeyError):
        tbl.drop("Invalid", axis="columns")

def test_qvd_table_drop_column_list():
    """
    Tests the functionality of dropping multiple columns from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.drop(["Value", "New"], axis="columns")

    assert tbl.shape == (3, 1)
    assert tbl.columns == ["Key"]

def test_qvd_table_drop_column_list_with_invalid_name():
    """
    Tests the functionality of dropping multiple invalid columns from a QVD table raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(KeyError):
        tbl.drop(["Value", "Invalid"], axis="columns")

    assert tbl.shape == (3, 3)

def test_qvd_table_drop_row():
    """
    Tests the functionality of dropping a row from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.drop(1)

    assert tbl.shape == (3, 2)
    assert tbl.at(0, "Key").display_value == 1
    assert tbl.at(1, "Key").display_value == 3
    assert tbl.at(2, "Key").display_value == 4

def test_qvd_table_drop_row_with_invalid_index():
    """
    Tests the functionality of dropping an invalid row from a QVD table raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(IndexError):
        tbl.drop(4)

def test_qvd_table_drop_row_list():
    """
    Tests the functionality of dropping multiple rows from a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    tbl.drop([0, 2])

    assert tbl.shape == (2, 2)
    assert tbl.at(0, "Key").display_value == 2
    assert tbl.at(1, "Key").display_value == 4

def test_qvd_table_drop_row_list_with_invalid_index():
    """
    Tests the functionality of dropping multiple invalid rows from a QVD table raises an exception.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    with pytest.raises(IndexError):
        tbl.drop([0, 4])

    assert tbl.shape == (4, 2)

def test_qvd_table_filter_by():
    """
    Tests the functionality of filtering a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "A"],
            [4, "B"],
            [5, "A"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    new_tbl = tbl.filter_by("Key", lambda x: x.calculation_value in [1, 3, 5])

    assert new_tbl.shape == (3, 2)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 3
    assert new_tbl.at(2, "Key").display_value == 5

def test_qvd_table_sort_by_asc():
    """
    Tests the functionality of sorting a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [1, "A"],
            [5, "E"],
            [2, "B"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    new_tbl = tbl.sort_by("Key")

    assert new_tbl.shape == (5, 2)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(3, "Key").display_value == 4
    assert new_tbl.at(4, "Key").display_value == 5

def test_qvd_table_sort_by_desc():
    """
    Tests the functionality of sorting a QVD table in descending order.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [1, "A"],
            [5, "E"],
            [2, "B"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    new_tbl = tbl.sort_by("Key", ascending=False)

    assert new_tbl.shape == (5, 2)
    assert new_tbl.at(0, "Key").display_value == 5
    assert new_tbl.at(1, "Key").display_value == 4
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(3, "Key").display_value == 2
    assert new_tbl.at(4, "Key").display_value == 1

def test_qvd_table_sort_by_custom_comparator():
    """
    Tests the functionality of sorting a QVD table with a custom comparator.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [1, "A"],
            [5, "E"],
            [2, "B"],
            [4, "D"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)
    new_tbl = tbl.sort_by("Value", comparator=(lambda x, y: 1 if x.calculation_value > y.calculation_value else
                                             -1 if x.calculation_value < y.calculation_value else 0))

    assert new_tbl.shape == (5, 2)
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "B"
    assert new_tbl.at(2, "Value").display_value == "C"
    assert new_tbl.at(3, "Value").display_value == "D"
    assert new_tbl.at(4, "Value").display_value == "E"

def test_qvd_table_concat():
    """
    Tests the functionality of concatenating two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [4, "D"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.concat(tbl2)

    assert new_tbl.shape == (4, 2)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(3, "Key").display_value == 4

def test_qvd_table_concat_different_columns():
    """
    Tests the functionality of concatenating two QVD tables with different columns.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "New"],
        "data": [
            [3, "C"],
            [4, "D"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.concat(tbl2)

    assert new_tbl.shape == (4, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(3, "Key").display_value == 4
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "B"
    assert new_tbl.at(0, "New") is None
    assert new_tbl.at(1, "New") is None
    assert new_tbl.at(2, "New").display_value == "C"
    assert new_tbl.at(3, "New").display_value == "D"

def test_qvd_table_left_join():
    """
    Tests the functionality of performing a left join on two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "New"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="left")

    assert new_tbl.shape == (3, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "B"
    assert new_tbl.at(2, "Value").display_value == "C"
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New") is None
    assert new_tbl.at(2, "New").display_value == "Y"

def test_qvd_table_left_join_with_multiple_keys():
    """
    Tests the functionality of performing a left join on two QVD tables with multiple keys.
    """
    raw_tbl1 = {
        "columns": ["Key1", "Key2", "Value"],
        "data": [
            [1, 1, "A"],
            [2, 2, "B"],
            [3, 3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key1", "Key2", "New"],
        "data": [
            [1, 1, "X"],
            [2, 4, "Y"],
            [3, 3, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on=["Key1", "Key2"], how="left")

    assert new_tbl.shape == (3, 4)
    assert new_tbl.at(0, "Key1").display_value == 1
    assert new_tbl.at(1, "Key1").display_value == 2
    assert new_tbl.at(2, "Key1").display_value == 3
    assert new_tbl.at(0, "Key2").display_value == 1
    assert new_tbl.at(1, "Key2").display_value == 2
    assert new_tbl.at(2, "Key2").display_value == 3
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "B"
    assert new_tbl.at(2, "Value").display_value == "C"
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New") is None
    assert new_tbl.at(2, "New").display_value == "Z"

def test_qvd_table_left_join_overlapping_columns():
    """
    Tests the functionality of performing a left join on two QVD tables with overlapping columns.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="left", lsuffix="_l", rsuffix="_r")

    assert new_tbl.shape == (3, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(0, "Value_l").display_value == "A"
    assert new_tbl.at(1, "Value_l").display_value == "B"
    assert new_tbl.at(2, "Value_l").display_value == "C"
    assert new_tbl.at(0, "Value_r").display_value == "X"
    assert new_tbl.at(1, "Value_r") is None
    assert new_tbl.at(2, "Value_r").display_value == "Y"

def test_qvd_table_left_join_overlapping_columns_without_suffixes():
    """
    Tests the functionality of performing a left join on two QVD tables with overlapping columns without suffixes.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)

    with pytest.raises(ValueError):
        tbl1.join(tbl2, on="Key", how="left")

def test_qvd_table_right_join():
    """
    Tests the functionality of performing a right join on two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "New"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="right")

    assert new_tbl.shape == (3, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 3
    assert new_tbl.at(2, "Key").display_value == 4
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "C"
    assert new_tbl.at(2, "Value") is None
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New").display_value == "Y"
    assert new_tbl.at(2, "New").display_value == "Z"

def test_qvd_table_right_join_with_overlapping_columns():
    """
    Tests the functionality of performing a right join on two QVD tables with overlapping columns.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="right", lsuffix="_l", rsuffix="_r")

    assert new_tbl.shape == (3, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 3
    assert new_tbl.at(2, "Key").display_value == 4
    assert new_tbl.at(0, "Value_l").display_value == "A"
    assert new_tbl.at(1, "Value_l").display_value == "C"
    assert new_tbl.at(2, "Value_l") is None
    assert new_tbl.at(0, "Value_r").display_value == "X"
    assert new_tbl.at(1, "Value_r").display_value == "Y"
    assert new_tbl.at(2, "Value_r").display_value == "Z"

def test_qvd_table_right_join_with_multiple_keys():
    """
    Tests the functionality of performing a right join on two QVD tables with multiple keys.
    """
    raw_tbl1 = {
        "columns": ["Key1", "Key2", "Value"],
        "data": [
            [1, 1, "A"],
            [2, 2, "B"],
            [3, 3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key1", "Key2", "New"],
        "data": [
            [1, 1, "X"],
            [2, 4, "Y"],
            [3, 3, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on=["Key1", "Key2"], how="right")

    assert new_tbl.shape == (3, 4)
    assert new_tbl.at(0, "Key1").display_value == 1
    assert new_tbl.at(1, "Key1").display_value == 2
    assert new_tbl.at(2, "Key1").display_value == 3
    assert new_tbl.at(0, "Key2").display_value == 1
    assert new_tbl.at(1, "Key2").display_value == 4
    assert new_tbl.at(2, "Key2").display_value == 3
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value") is None
    assert new_tbl.at(2, "Value").display_value == "C"
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New").display_value == "Y"
    assert new_tbl.at(2, "New").display_value == "Z"

def test_qvd_table_inner_join():
    """
    Tests the functionality of performing an inner join on two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "New"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="inner")

    assert new_tbl.shape == (2, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 3
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "C"
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New").display_value == "Y"

def test_qvd_table_inner_join_with_multiple_keys():
    """
    Tests the functionality of performing an inner join on two QVD tables with multiple keys.
    """
    raw_tbl1 = {
        "columns": ["Key1", "Key2", "Value"],
        "data": [
            [1, 1, "A"],
            [2, 2, "B"],
            [3, 3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key1", "Key2", "New"],
        "data": [
            [1, 1, "X"],
            [2, 4, "Y"],
            [3, 3, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on=["Key1", "Key2"], how="inner")

    assert new_tbl.shape == (2, 4)
    assert new_tbl.at(0, "Key1").display_value == 1
    assert new_tbl.at(1, "Key1").display_value == 3
    assert new_tbl.at(0, "Key2").display_value == 1
    assert new_tbl.at(1, "Key2").display_value == 3
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "C"
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New").display_value == "Z"

def test_qvd_table_inner_join_overlapping_columns():
    """
    Tests the functionality of performing an inner join on two QVD tables with overlapping columns.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="inner", lsuffix="_l", rsuffix="_r")

    assert new_tbl.shape == (2, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 3
    assert new_tbl.at(0, "Value_l").display_value == "A"
    assert new_tbl.at(1, "Value_l").display_value == "C"
    assert new_tbl.at(0, "Value_r").display_value == "X"
    assert new_tbl.at(1, "Value_r").display_value == "Y"

def test_qvd_table_outer_join():
    """
    Tests the functionality of performing an outer join on two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "New"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="outer")

    assert new_tbl.shape == (4, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(3, "Key").display_value == 4
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "B"
    assert new_tbl.at(2, "Value").display_value == "C"
    assert new_tbl.at(3, "Value") is None
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New") is None
    assert new_tbl.at(2, "New").display_value == "Y"
    assert new_tbl.at(3, "New").display_value == "Z"

def test_qvd_table_outer_join_with_multiple_keys():
    """
    Tests the functionality of performing an outer join on two QVD tables with multiple keys.
    """
    raw_tbl1 = {
        "columns": ["Key1", "Key2", "Value"],
        "data": [
            [1, 1, "A"],
            [2, 2, "B"],
            [3, 3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key1", "Key2", "New"],
        "data": [
            [1, 1, "X"],
            [2, 4, "Y"],
            [3, 3, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on=["Key1", "Key2"], how="outer")

    assert new_tbl.shape == (4, 4)
    assert new_tbl.at(0, "Key1").display_value == 1
    assert new_tbl.at(1, "Key1").display_value == 2
    assert new_tbl.at(2, "Key1").display_value == 3
    assert new_tbl.at(3, "Key1").display_value == 2
    assert new_tbl.at(0, "Key2").display_value == 1
    assert new_tbl.at(1, "Key2").display_value == 2
    assert new_tbl.at(2, "Key2").display_value == 3
    assert new_tbl.at(3, "Key2").display_value == 4
    assert new_tbl.at(0, "Value").display_value == "A"
    assert new_tbl.at(1, "Value").display_value == "B"
    assert new_tbl.at(2, "Value").display_value == "C"
    assert new_tbl.at(3, "Value") is None
    assert new_tbl.at(0, "New").display_value == "X"
    assert new_tbl.at(1, "New") is None
    assert new_tbl.at(2, "New").display_value == "Z"
    assert new_tbl.at(3, "New").display_value == "Y"

def test_qvd_table_outer_join_overlapping_columns():
    """
    Tests the functionality of performing an outer join on two QVD tables with overlapping columns.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "X"],
            [3, "Y"],
            [4, "Z"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)
    new_tbl = tbl1.join(tbl2, on="Key", how="outer", lsuffix="_l", rsuffix="_r")

    assert new_tbl.shape == (4, 3)
    assert new_tbl.at(0, "Key").display_value == 1
    assert new_tbl.at(1, "Key").display_value == 2
    assert new_tbl.at(2, "Key").display_value == 3
    assert new_tbl.at(3, "Key").display_value == 4
    assert new_tbl.at(0, "Value_l").display_value == "A"
    assert new_tbl.at(1, "Value_l").display_value == "B"
    assert new_tbl.at(2, "Value_l").display_value == "C"
    assert new_tbl.at(3, "Value_l") is None
    assert new_tbl.at(0, "Value_r").display_value == "X"
    assert new_tbl.at(1, "Value_r") is None
    assert new_tbl.at(2, "Value_r").display_value == "Y"
    assert new_tbl.at(3, "Value_r").display_value == "Z"

def test_qvd_table_at():
    """
    Tests the at functionality of a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    assert tbl.at(0, "Key").display_value == 1
    assert tbl.at(0, "Value").display_value == "A"
    assert tbl.at(1, "Key").display_value == 2
    assert tbl.at(1, "Value").display_value == "B"
    assert tbl.at(2, "Key").display_value == 3
    assert tbl.at(2, "Value").display_value == "C"
    assert tbl.at(3, "Key").display_value == 4
    assert tbl.at(3, "Value").display_value == "D"
    assert tbl.at(4, "Key").display_value == 5
    assert tbl.at(4, "Value").display_value == "E"

def test_qvd_table_head():
    """
    Tests the head functionality of a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    head_tbl = tbl.head(2)

    assert head_tbl.shape == (2, 2)
    assert head_tbl.at(0, "Key").display_value == 1
    assert head_tbl.at(0, "Value").display_value == "A"
    assert head_tbl.at(1, "Key").display_value == 2
    assert head_tbl.at(1, "Value").display_value == "B"

def test_qvd_table_tail():
    """
    Tests the tail functionality of a QVD table.
    """
    raw_tbl = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl = QvdTable.from_dict(raw_tbl)

    tail_tbl = tbl.tail(2)

    assert tail_tbl.shape == (2, 2)
    assert tail_tbl.at(0, "Key").display_value == 4
    assert tail_tbl.at(0, "Value").display_value == "D"
    assert tail_tbl.at(1, "Key").display_value == 5
    assert tail_tbl.at(1, "Value").display_value == "E"

def test_qvd_table_eq():
    """
    Tests the equality of two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)

    assert tbl1 == tbl2

def test_qvd_table_ne():
    """
    Tests the inequality of two QVD tables.
    """
    raw_tbl1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    raw_tbl2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "F"]
        ]
    }

    tbl1 = QvdTable.from_dict(raw_tbl1)
    tbl2 = QvdTable.from_dict(raw_tbl2)

    assert tbl1 != tbl2
