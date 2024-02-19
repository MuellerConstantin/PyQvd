import os
import time
import pytest
from pyqvd.qvd import QvdFile

def test_parse_well_formed_qvd_file():
    file = QvdFile.load(os.path.join(os.path.dirname(__file__), 'data/small.qvd'))

    assert file is not None
    assert file.number_of_rows == 606
    assert len(file.field_names) == 8
    assert 'small.qvd' in file.path
    assert file.get_row(0) is not None
    assert file.get_row(605) is not None

def test_parse_qvd_file_with_1000_rows():
    start = int(time.time() * 1000)
    QvdFile.load(os.path.join(os.path.dirname(__file__), 'data/small.qvd'))
    end = int(time.time() * 1000)

    assert end - start < 250

def test_parse_qvd_file_with_20000_rows():
    start = int(time.time() * 1000)
    QvdFile.load(os.path.join(os.path.dirname(__file__), 'data/medium.qvd'))
    end = int(time.time() * 1000)

    assert end - start < 2500

def test_parse_qvd_file_with_60000_rows():
    start = int(time.time() * 1000)
    QvdFile.load(os.path.join(os.path.dirname(__file__), 'data/large.qvd'))
    end = int(time.time() * 1000)

    assert end - start < 5000

def test_parse_damaged_qvd_file():
    with pytest.raises(Exception):
        QvdFile.load(os.path.join(os.path.dirname(__file__), 'data/damaged.qvd'))
