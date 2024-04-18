"""
Tests the functionality related to persisting files.
"""

import os
from pyqvd import QvdDataFrame

def test_write_qvd_file(tmp_path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to file successfully.
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

    df = QvdDataFrame.from_dict(raw_df)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 2
    assert df.columns is not None
    assert len(df.columns) == 2
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 2)

    df.to_qvd(str(tmp_path / 'written.qvd'))

    assert os.path.exists(str(tmp_path / 'written.qvd'))
    assert os.path.getsize(str(tmp_path / 'written.qvd')) > 0

    written_df = QvdDataFrame.from_qvd(str(tmp_path / 'written.qvd'))

    assert written_df is not None
    assert written_df.shape is not None
    assert written_df.shape[0] == 5
    assert written_df.shape[1] == 2

    written_columns = written_df.to_dict()["columns"]
    written_data = written_df.to_dict()["data"]

    assert written_columns == ['Key', 'Value']
    assert written_data[0] == [1, 'A']
    assert written_data[1] == [2, 'B']
    assert written_data[2] == [3, 'C']
    assert written_data[3] == [4, 'D']
    assert written_data[4] == [5, 'E']

def test_write_qvd_file_as_binary_file_stream(tmp_path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to a binary stream successfully.
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

    df = QvdDataFrame.from_dict(raw_df)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 2
    assert df.columns is not None
    assert len(df.columns) == 2
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 2)

    with open(str(tmp_path / 'written.qvd'), 'wb') as file:
        df.to_stream(file)

    assert os.path.exists(tmp_path / 'written.qvd')
    assert os.path.getsize(tmp_path / 'written.qvd') > 0

    written_df = QvdDataFrame.from_qvd(str(tmp_path / 'written.qvd'))

    assert written_df is not None
    assert written_df.shape is not None
    assert written_df.shape[0] == 5
    assert written_df.shape[1] == 2

    written_columns = written_df.to_dict()["columns"]
    written_data = written_df.to_dict()["data"]

    assert written_columns == ['Key', 'Value']
    assert written_data[0] == [1, 'A']
    assert written_data[1] == [2, 'B']
    assert written_data[2] == [3, 'C']
    assert written_data[3] == [4, 'D']
    assert written_data[4] == [5, 'E']
