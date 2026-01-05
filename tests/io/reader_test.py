"""
Tests the functionality related to reading files.
"""

import os
import pytest
from pyqvd import QvdTable

def test_read_qvd_file_with_1000_rows():
    """
    Tests if a small QVD file can be parsed properly.
    """
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/small.qvd"))

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 1000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 1000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_with_20000_rows():
    """
    Tests if a medium QVD file can be parsed properly.
    """
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/medium.qvd"))

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 20000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 20000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_with_60000_rows():
    """
    Tests if a large QVD file can be parsed properly.
    """
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/large.qvd"))

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 200000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 200000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_in_chunks():
    """
    Tests if a large QVD file can be parsed properly in chunks.
    """
    itr = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/medium.qvd"), chunk_size=5000)

    assert itr is not None
    assert len(itr) == 4

    total_tbl = None

    for tbl in itr:
        if total_tbl is None:
            total_tbl = tbl
        else:
            total_tbl = total_tbl.concat(tbl)

    assert total_tbl is not None
    assert total_tbl.shape is not None
    assert total_tbl.shape[0] == 20000
    assert total_tbl.shape[1] == 6
    assert total_tbl.columns is not None
    assert len(total_tbl.columns) == 6
    assert total_tbl.data is not None
    assert len(total_tbl.data) == 20000
    assert total_tbl.head(5).shape == (5, 6)

def test_read_damaged_qvd_file():
    """
    Tests if reading a damaged QVD file fails as expected.
    """
    with pytest.raises(Exception):
        QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/damaged.qvd"))

def test_read_binary_file_stream_in_chunks():
    """
    Tests if QVD table can be read from a binary file stream properly in chunks.
    """
    with open(os.path.join(os.path.dirname(__file__), "../data/medium.qvd"), "rb") as file:
        itr = QvdTable.from_stream(file, chunk_size=5000)

        assert itr is not None
        assert len(itr) == 4

        total_tbl = None

        for tbl in itr:
            if total_tbl is None:
                total_tbl = tbl
            else:
                total_tbl = total_tbl.concat(tbl)

        assert total_tbl is not None
        assert total_tbl.shape is not None
        assert total_tbl.shape[0] == 20000
        assert total_tbl.shape[1] == 6
        assert total_tbl.columns is not None
        assert len(total_tbl.columns) == 6
        assert total_tbl.data is not None
        assert len(total_tbl.data) == 20000
        assert total_tbl.head(5).shape == (5, 6)

def test_read_binary_file_stream():
    """
    Tests if QVD table can be read from a binary file stream properly.
    """
    with open(os.path.join(os.path.dirname(__file__), "../data/small.qvd"), "rb") as file:
        df = QvdTable.from_stream(file)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 1000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 1000
    assert df.head(5).shape == (5, 6)
