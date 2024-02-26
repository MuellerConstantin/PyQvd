import os
import time
import pytest
from pyqvd import QvdDataFrame

def test_parse_qvd_file_with_1000_rows():
    start = int(time.time() * 1000)
    df = QvdDataFrame.from_qvd(os.path.join(os.path.dirname(__file__), 'data/small.qvd'))
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

def test_parse_qvd_file_with_20000_rows():
    start = int(time.time() * 1000)
    df = QvdDataFrame.from_qvd(os.path.join(os.path.dirname(__file__), 'data/medium.qvd'))
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

def test_parse_qvd_file_with_60000_rows():
    start = int(time.time() * 1000)
    df = QvdDataFrame.from_qvd(os.path.join(os.path.dirname(__file__), 'data/large.qvd'))
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

def test_parse_damaged_qvd_file():
    with pytest.raises(Exception):
        QvdDataFrame.from_qvd(os.path.join(os.path.dirname(__file__), 'data/damaged.qvd'))
