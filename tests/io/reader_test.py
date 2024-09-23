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
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/small.qvd"))
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
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/medium.qvd"))
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
    df = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/large.qvd"))
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

def test_read_qvd_file_in_chunks():
    """
    Tests if a large QVD file can be parsed properly in chunks.
    """
    itr = QvdTable.from_qvd(os.path.join(os.path.dirname(__file__), "../data/medium.qvd"), chunk_size=5000)

    assert itr is not None
    assert len(itr) == 4

    total_tbl = None

    start = int(time.time() * 1000)

    for tbl in itr:
        if total_tbl is None:
            total_tbl = tbl
        else:
            total_tbl = total_tbl.concat(tbl)

    end = int(time.time() * 1000)

    assert end - start < 10000
    assert total_tbl is not None
    assert total_tbl.shape is not None
    assert total_tbl.shape[0] == 18484
    assert total_tbl.shape[1] == 13
    assert total_tbl.columns is not None
    assert len(total_tbl.columns) == 13
    assert total_tbl.data is not None
    assert len(total_tbl.data) == 18484
    assert total_tbl.head(5).shape == (5, 13)

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

        start = int(time.time() * 1000)

        for tbl in itr:
            if total_tbl is None:
                total_tbl = tbl
            else:
                total_tbl = total_tbl.concat(tbl)

        end = int(time.time() * 1000)

        assert end - start < 10000
        assert total_tbl is not None
        assert total_tbl.shape is not None
        assert total_tbl.shape[0] == 18484
        assert total_tbl.shape[1] == 13
        assert total_tbl.columns is not None
        assert len(total_tbl.columns) == 13
        assert total_tbl.data is not None
        assert len(total_tbl.data) == 18484
        assert total_tbl.head(5).shape == (5, 13)

def test_read_binary_file_stream():
    """
    Tests if QVD table can be read from a binary file stream properly.
    """
    with open(os.path.join(os.path.dirname(__file__), "../data/small.qvd"), "rb") as file:
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
