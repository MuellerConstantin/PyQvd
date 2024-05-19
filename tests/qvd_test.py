"""
Tests the functionality related to reading files.
"""

import pytest
from typing import TYPE_CHECKING
from pyqvd import QvdTable, IntegerValue, StringValue

if TYPE_CHECKING:
    import pandas as pd

def test_construct_qvd_table_from_dict():
    """
    Tests if a QVD table, constructed from a dictionary, can be read properly.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
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
        'Key': [1, 2, 3, 4, 5],
        'Value': ['A', 'B', 'C', 'D', 'E']
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
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
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
        'Key': [1, 2, 3, 4, 5],
        'Value': ['A', 'B', 'C', 'D', 'E']
    })

    df = QvdTable.from_pandas(raw_df)

    assert df.to_pandas().equals(raw_df)

def test_construct_qvd_table_directly():
    """
    Tests if a QVD table can be constructed directly.
    """
    df = QvdTable(
        columns=['Key', 'Value'],
        data=[
            [IntegerValue(1), StringValue('A')],
            [IntegerValue(2), StringValue('B')],
            [IntegerValue(3), StringValue('C')],
            [IntegerValue(4), StringValue('D')],
            [IntegerValue(5), StringValue('E')]
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
            columns=['Key', 'Value'],
            data=[
                [IntegerValue(1), StringValue('A')],
                [IntegerValue(2)],
                [IntegerValue(3), StringValue('C')]
            ]
        )

def test_qvd_table_get_column():
    """
    Tests the functionality of getting a column from a QVD table.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df.get('Key')

    assert values is not None
    assert len(values) == 5
    assert values[0].display_value == 1
    assert values[1].display_value == 2
    assert values[2].display_value == 3
    assert values[3].display_value == 4
    assert values[4].display_value == 5

def test_qvd_table_get_row():
    """
    Tests the functionality of getting a row from a QVD table.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df.get(0)

    assert values is not None
    assert len(values) == 2
    assert values[0].display_value == 1
    assert values[1].display_value == 'A'

def test_qvd_table_getitem_by_column():
    """
    Tests the functionality of getting a column from a QVD table using the getitem method.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df['Key']

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
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)
    values = df[0]

    assert values is not None
    assert len(values) == 2
    assert values[0].display_value == 1
    assert values[1].display_value == 'A'

def test_qvd_table_at():
    """
    Tests the at functionality of a QVD table.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)

    assert df.at(0, 'Key').display_value == 1
    assert df.at(0, 'Value').display_value == 'A'
    assert df.at(1, 'Key').display_value == 2
    assert df.at(1, 'Value').display_value == 'B'
    assert df.at(2, 'Key').display_value == 3
    assert df.at(2, 'Value').display_value == 'C'
    assert df.at(3, 'Key').display_value == 4
    assert df.at(3, 'Value').display_value == 'D'
    assert df.at(4, 'Key').display_value == 5
    assert df.at(4, 'Value').display_value == 'E'

def test_qvd_table_head():
    """
    Tests the head functionality of a QVD table.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)

    head_df = df.head(2)

    assert head_df.shape == (2, 2)
    assert head_df.at(0, 'Key').display_value == 1
    assert head_df.at(0, 'Value').display_value == 'A'
    assert head_df.at(1, 'Key').display_value == 2
    assert head_df.at(1, 'Value').display_value == 'B'

def test_qvd_table_tail():
    """
    Tests the tail functionality of a QVD table.
    """
    raw_df = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    df = QvdTable.from_dict(raw_df)

    tail_df = df.tail(2)

    assert tail_df.shape == (2, 2)
    assert tail_df.at(0, 'Key').display_value == 4
    assert tail_df.at(0, 'Value').display_value == 'D'
    assert tail_df.at(1, 'Key').display_value == 5
    assert tail_df.at(1, 'Value').display_value == 'E'

def test_qvd_table_eq():
    """
    Tests the equality of two QVD tables.
    """
    raw_df1 = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    raw_df2 = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
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
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'E']
        ]
    }

    raw_df2 = {
        'columns': ['Key', 'Value'],
        'data': [
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
            [5, 'F']
        ]
    }

    df1 = QvdTable.from_dict(raw_df1)
    df2 = QvdTable.from_dict(raw_df2)

    assert df1 != df2
