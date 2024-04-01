"""
Tests the functionality related to persisting files.
"""

import os
from pyqvd import QvdDataFrame

def test_write_qvd_file():
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

    df.to_qvd('tests/data/written.qvd')

    assert os.path.exists('tests/data/written.qvd')
    assert os.path.getsize('tests/data/written.qvd') > 0

    os.remove('tests/data/written.qvd')