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
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 2
    assert df.columns is not None
    assert len(df.columns) == 2
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 2)
    assert df.to_dict() == raw_df

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

    df = QvdTable.from_pandas(raw_df)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 2
    assert df.columns is not None
    assert len(df.columns) == 2
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 2)
    assert df.to_pandas().equals(raw_df)

def test_qvd_table_to_dict():
    """
    Tests if a QVD table can be converted to a dictionary properly.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    assert df.to_dict() == raw_df

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

    df = QvdTable.from_pandas(raw_df)

    assert df.to_pandas().equals(raw_df)

def test_construct_qvd_table_directly():
    """
    Tests if a QVD table can be constructed directly.
    """
    df = QvdTable(
        columns=["Key", "Value"],
        data=[
            [IntegerValue(1), StringValue("A")],
            [IntegerValue(2), StringValue("B")],
            [IntegerValue(3), StringValue("C")],
            [IntegerValue(4), StringValue("D")],
            [IntegerValue(5), StringValue("E")]
        ]
    )

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 2
    assert df.columns is not None
    assert len(df.columns) == 2
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 2)

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
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    value = df.get((0, "Key"))

    assert value is not None
    assert value.display_value == 1

def test_qvd_table_get_by_invalid_tuple():
    """
    Tests the functionality of getting an invalid cell from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(IndexError):
        df.get((5, "Key"))

def test_qvd_table_get_by_column():
    """
    Tests the functionality of getting a column from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df.get("Key")

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
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(KeyError):
        df.get("Invalid")

def test_qvd_table_get_by_row():
    """
    Tests the functionality of getting a row from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df.get(0)

    assert values is not None
    assert len(values) == 2
    assert values[0].display_value == 1
    assert values[1].display_value == "A"

def test_qvd_table_get_by_invalid_row():
    """
    Tests the functionality of getting an invalid row from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(IndexError):
        df.get(5)

def test_qvd_table_get_by_slice():
    """
    Tests the functionality of getting a slice from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df.get(slice(0, 2))

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
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    value = df[0, "Key"]

    assert value is not None
    assert value.display_value == 1

def test_qvd_table_getitem_by_column():
    """
    Tests the functionality of getting a column from a QVD table using the getitem method.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df["Key"]

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
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df[0]

    assert values is not None
    assert len(values) == 2
    assert values[0].display_value == 1
    assert values[1].display_value == "A"

def test_qvd_table_getitem_by_slice():
    """
    Tests the functionality of getting a slice from a QVD table using the getitem method.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df[0:2]

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
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.set("Key", [IntegerValue(6), IntegerValue(7), IntegerValue(8), IntegerValue(9), IntegerValue(10)])

    assert df.at(0, "Key").display_value == 6
    assert df.at(1, "Key").display_value == 7
    assert df.at(2, "Key").display_value == 8
    assert df.at(3, "Key").display_value == 9
    assert df.at(4, "Key").display_value == 10

def test_qvd_table_add_column():
    """
    Tests the functionality of adding a column to a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.set("New", [IntegerValue(4), IntegerValue(5), IntegerValue(6)])

    assert df.shape == (3, 3)
    assert df.at(0, "New").display_value == 4
    assert df.at(1, "New").display_value == 5
    assert df.at(2, "New").display_value == 6

def test_qvd_table_set_by_column_with_invalid_shape():
    """
    Tests the functionality of setting a column in a QVD table with invalid data raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(ValueError):
        df.set("Key", [IntegerValue(6), IntegerValue(7), IntegerValue(8)])

def test_qvd_table_set_by_row():
    """
    Tests the functionality of setting a row in a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.set(0, [IntegerValue(6), StringValue("F")])

    assert df.at(0, "Key").display_value == 6
    assert df.at(0, "Value").display_value == "F"

def test_qvd_table_set_by_invalid_row():
    """
    Tests the functionality of setting an invalid row in a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(IndexError):
        df.set(5, [IntegerValue(6), StringValue("F")])

def test_qvd_table_set_by_row_with_invalid_shape():
    """
    Tests the functionality of setting a row in a QVD table with invalid data raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(ValueError):
        df.set(0, [IntegerValue(6)])

def test_qvd_table_set_by_slice():
    """
    Tests the functionality of setting a slice in a QVD table.
    """
    raw_df = {
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

    df = QvdTable.from_dict(raw_df)
    df.set(slice(1, 4), new_data)

    assert df.at(1, "Key").display_value == 6
    assert df.at(1, "Value").display_value == "F"
    assert df.at(2, "Key").display_value == 7
    assert df.at(2, "Value").display_value == "G"
    assert df.at(3, "Key").display_value == 8
    assert df.at(3, "Value").display_value == "H"

def test_qvd_table_set_by_slice_with_invalid_shape():
    """
    Tests the functionality of setting a slice in a QVD table with invalid data raises an exception.
    """
    raw_df = {
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

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(ValueError):
        df.set(slice(1, 4), new_data)

def test_qvd_table_setitem_by_column():
    """
    Tests the functionality of setting a column in a QVD table using the setitem method.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df["Key"] = [IntegerValue(6), IntegerValue(7), IntegerValue(8), IntegerValue(9), IntegerValue(10)]

    assert df.at(0, "Key").display_value == 6
    assert df.at(1, "Key").display_value == 7
    assert df.at(2, "Key").display_value == 8
    assert df.at(3, "Key").display_value == 9
    assert df.at(4, "Key").display_value == 10

def test_qvd_table_setitem_add_column():
    """
    Tests the functionality of adding a column to a QVD table using the setitem method.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df["New"] = [IntegerValue(4), IntegerValue(5), IntegerValue(6)]

    assert df.shape == (3, 3)
    assert df.at(0, "New").display_value == 4
    assert df.at(1, "New").display_value == 5
    assert df.at(2, "New").display_value == 6

def test_qvd_table_setitem_by_row():
    """
    Tests the functionality of setting a row in a QVD table using the setitem method.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df[0] = [IntegerValue(6), StringValue("F")]

    assert df.at(0, "Key").display_value == 6
    assert df.at(0, "Value").display_value == "F"

def test_qvd_table_setitem_by_slice():
    """
    Tests the functionality of setting a slice in a QVD table using the setitem method.
    """
    raw_df = {
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

    df = QvdTable.from_dict(raw_df)
    df[1:4] = new_data

    assert df.at(1, "Key").display_value == 6
    assert df.at(1, "Value").display_value == "F"
    assert df.at(2, "Key").display_value == 7
    assert df.at(2, "Value").display_value == "G"
    assert df.at(3, "Key").display_value == 8
    assert df.at(3, "Value").display_value == "H"

def test_qvd_table_append_row():
    """
    Tests the functionality of appending a row to a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.append([IntegerValue(2), StringValue("B")])

    assert df.shape == (2, 2)
    assert df.at(1, "Key").display_value == 2
    assert df.at(1, "Value").display_value == "B"

def test_qvd_table_append_row_with_invalid_shape():
    """
    Tests the functionality of appending a row to a QVD table with invalid data raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(ValueError):
        df.append([IntegerValue(2)])

def test_qvd_table_insert_row():
    """
    Tests the functionality of inserting a row to a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.insert(0, [IntegerValue(1), StringValue("A")])

    assert df.shape == (5, 2)
    assert df.at(0, "Key").display_value == 1
    assert df.at(0, "Value").display_value == "A"

def test_qvd_table_insert_row_with_invalid_shape():
    """
    Tests the functionality of inserting a row to a QVD table with invalid data raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(ValueError):
        df.insert(0, [IntegerValue(1)])

def test_qvd_table_insert_row_with_invalid_index():
    """
    Tests the functionality of inserting a row to a QVD table with an invalid index raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(IndexError):
        df.insert(5, [IntegerValue(1), StringValue("A")])

def test_qvd_table_drop_column():
    """
    Tests the functionality of dropping a column from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.drop("New", axis="columns")

    assert df.shape == (3, 2)
    assert df.columns == ["Key", "Value"]

def test_qvd_table_drop_column_with_invalid_name():
    """
    Tests the functionality of dropping an invalid column from a QVD table raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(KeyError):
        df.drop("Invalid", axis="columns")

def test_qvd_table_drop_column_list():
    """
    Tests the functionality of dropping multiple columns from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.drop(["Value", "New"], axis="columns")

    assert df.shape == (3, 1)
    assert df.columns == ["Key"]

def test_qvd_table_drop_column_list_with_invalid_name():
    """
    Tests the functionality of dropping multiple invalid columns from a QVD table raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value", "New"],
        "data": [
            [1, "A", "X"],
            [2, "B", "Y"],
            [3, "C", "Z"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(KeyError):
        df.drop(["Value", "Invalid"], axis="columns")

    assert df.shape == (3, 3)

def test_qvd_table_drop_row():
    """
    Tests the functionality of dropping a row from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.drop(1)

    assert df.shape == (3, 2)
    assert df.at(0, "Key").display_value == 1
    assert df.at(1, "Key").display_value == 3
    assert df.at(2, "Key").display_value == 4

def test_qvd_table_drop_row_with_invalid_index():
    """
    Tests the functionality of dropping an invalid row from a QVD table raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(IndexError):
        df.drop(4)

def test_qvd_table_drop_row_list():
    """
    Tests the functionality of dropping multiple rows from a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    df.drop([0, 2])

    assert df.shape == (2, 2)
    assert df.at(0, "Key").display_value == 2
    assert df.at(1, "Key").display_value == 4

def test_qvd_table_drop_row_list_with_invalid_index():
    """
    Tests the functionality of dropping multiple invalid rows from a QVD table raises an exception.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    with pytest.raises(IndexError):
        df.drop([0, 4])

    assert df.shape == (4, 2)

def test_qvd_table_filter_by():
    """
    Tests the functionality of filtering a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "A"],
            [4, "B"],
            [5, "A"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    new_df = df.filter_by("Key", lambda x: x.calculation_value in [1, 3, 5])

    assert new_df.shape == (3, 2)
    assert new_df.at(0, "Key").display_value == 1
    assert new_df.at(1, "Key").display_value == 3
    assert new_df.at(2, "Key").display_value == 5

def test_qvd_table_sort_by_asc():
    """
    Tests the functionality of sorting a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [1, "A"],
            [5, "E"],
            [2, "B"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    new_df = df.sort_by("Key")

    assert new_df.shape == (5, 2)
    assert new_df.at(0, "Key").display_value == 1
    assert new_df.at(1, "Key").display_value == 2
    assert new_df.at(2, "Key").display_value == 3
    assert new_df.at(3, "Key").display_value == 4
    assert new_df.at(4, "Key").display_value == 5

def test_qvd_table_sort_by_desc():
    """
    Tests the functionality of sorting a QVD table in descending order.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [1, "A"],
            [5, "E"],
            [2, "B"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    new_df = df.sort_by("Key", ascending=False)

    assert new_df.shape == (5, 2)
    assert new_df.at(0, "Key").display_value == 5
    assert new_df.at(1, "Key").display_value == 4
    assert new_df.at(2, "Key").display_value == 3
    assert new_df.at(3, "Key").display_value == 2
    assert new_df.at(4, "Key").display_value == 1

def test_qvd_table_sort_by_custom_comparator():
    """
    Tests the functionality of sorting a QVD table with a custom comparator.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [3, "C"],
            [1, "A"],
            [5, "E"],
            [2, "B"],
            [4, "D"]
        ]
    }

    df = QvdTable.from_dict(raw_df)
    new_df = df.sort_by("Value", comparator=(lambda x, y: 1 if x.calculation_value > y.calculation_value else
                                             -1 if x.calculation_value < y.calculation_value else 0))

    assert new_df.shape == (5, 2)
    assert new_df.at(0, "Value").display_value == "A"
    assert new_df.at(1, "Value").display_value == "B"
    assert new_df.at(2, "Value").display_value == "C"
    assert new_df.at(3, "Value").display_value == "D"
    assert new_df.at(4, "Value").display_value == "E"

def test_qvd_table_at():
    """
    Tests the at functionality of a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    assert df.at(0, "Key").display_value == 1
    assert df.at(0, "Value").display_value == "A"
    assert df.at(1, "Key").display_value == 2
    assert df.at(1, "Value").display_value == "B"
    assert df.at(2, "Key").display_value == 3
    assert df.at(2, "Value").display_value == "C"
    assert df.at(3, "Key").display_value == 4
    assert df.at(3, "Value").display_value == "D"
    assert df.at(4, "Key").display_value == 5
    assert df.at(4, "Value").display_value == "E"

def test_qvd_table_head():
    """
    Tests the head functionality of a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    head_df = df.head(2)

    assert head_df.shape == (2, 2)
    assert head_df.at(0, "Key").display_value == 1
    assert head_df.at(0, "Value").display_value == "A"
    assert head_df.at(1, "Key").display_value == 2
    assert head_df.at(1, "Value").display_value == "B"

def test_qvd_table_tail():
    """
    Tests the tail functionality of a QVD table.
    """
    raw_df = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    tail_df = df.tail(2)

    assert tail_df.shape == (2, 2)
    assert tail_df.at(0, "Key").display_value == 4
    assert tail_df.at(0, "Value").display_value == "D"
    assert tail_df.at(1, "Key").display_value == 5
    assert tail_df.at(1, "Value").display_value == "E"

def test_qvd_table_eq():
    """
    Tests the equality of two QVD tables.
    """
    raw_df1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    raw_df2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    df1 = QvdTable.from_dict(raw_df1)
    df2 = QvdTable.from_dict(raw_df2)

    assert df1 == df2

def test_qvd_table_ne():
    """
    Tests the inequality of two QVD tables.
    """
    raw_df1 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "E"]
        ]
    }

    raw_df2 = {
        "columns": ["Key", "Value"],
        "data": [
            [1, "A"],
            [2, "B"],
            [3, "C"],
            [4, "D"],
            [5, "F"]
        ]
    }

    df1 = QvdTable.from_dict(raw_df1)
    df2 = QvdTable.from_dict(raw_df2)

    assert df1 != df2
