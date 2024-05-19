"""
Tests the functionality related to reading files.
"""

from typing import TYPE_CHECKING
from pyqvd import QvdTable

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

def test_qvd_table_at():
    """
    Tests the basic functionality of a QVD table.
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
    Tests the basic functionality of a QVD table.
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
    Tests the basic functionality of a QVD table.
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
