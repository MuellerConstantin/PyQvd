"""
Tests the functionality related to reading files.
"""

import os
import time
import pytest
from pyqvd import QvdTable

def test_read_qvd_file_with_1000_rows():
    """
    Tests if a small QVD file can be parsed properly.
    """
    start = int(time.time() * 1000)
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), 'data/small.qvd'))
    end = int(time.time() * 1000)

    assert end - start < 250
    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 606
    assert df.shape[1] == 8
    assert df.columns is not None
    assert len(df.columns) == 8
    assert df.data is not None
    assert len(df.data) == 606
    assert df.head(5).shape == (5, 8)

def test_read_qvd_file_with_20000_rows():
    """
    Tests if a medium QVD file can be parsed properly.
    """
    start = int(time.time() * 1000)
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), 'data/medium.qvd'))
    end = int(time.time() * 1000)

    assert end - start < 2500
    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 18484
    assert df.shape[1] == 13
    assert df.columns is not None
    assert len(df.columns) == 13
    assert df.data is not None
    assert len(df.data) == 18484
    assert df.head(5).shape == (5, 13)

def test_read_qvd_file_with_60000_rows():
    """
    Tests if a large QVD file can be parsed properly.
    """
    start = int(time.time() * 1000)
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), 'data/large.qvd'))
    end = int(time.time() * 1000)

    assert end - start < 5000
    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 60398
    assert df.shape[1] == 11
    assert df.columns is not None
    assert len(df.columns) == 11
    assert df.data is not None
    assert len(df.data) == 60398
    assert df.head(5).shape == (5, 11)

def test_read_damaged_qvd_file():
    """
    Tests if reading a damaged QVD file fails as expected.
    """
    with pytest.raises(Exception):
        QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), 'data/damaged.qvd'))

def test_read_binary_file_stream():
    """
    Tests if a binary file stream can be read properly.
    """
    with open(os.path.join(os.path.dirname(__file__), 'data/small.qvd'), 'rb') as file:
        df = QvdTable.from_stream(file)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 606
    assert df.shape[1] == 8
    assert df.columns is not None
    assert len(df.columns) == 8
    assert df.data is not None
    assert len(df.data) == 606
    assert df.head(5).shape == (5, 8)

def test_construct_qvd_file_from_dict():
    """
    Tests if a data frame, constructed from a dictionary, can be read properly.
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
