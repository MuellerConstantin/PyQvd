"""
Tests the functionality related to persisting files.
"""

import os
import datetime as dt
from decimal import Decimal
from pyqvd import QvdTable

def test_write_qvd_file(tmp_path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to file successfully.
    """
    raw_df = {
        "columns": ["Key", "Value", "Timestamp", "Duration", "Salary"],
        "data": [
            [1, "A", dt.datetime(2021, 1, 1, 0, 0, 0), dt.timedelta(days=1, seconds=3620), Decimal("1000.00")],
            [2, "B", dt.datetime(2021, 1, 2, 0, 0, 0), dt.timedelta(days=2, seconds=7240), Decimal("2000.00")],
            [3, "C", dt.datetime(2021, 1, 3, 0, 0, 0), dt.timedelta(days=3, seconds=7200), Decimal("3000.00")],
            [4, "D", dt.datetime(2021, 1, 4, 0, 0, 0), dt.timedelta(days=4, seconds=10800), Decimal("4000.00")],
            [5, "E", dt.datetime(2021, 1, 5, 0, 0, 0), dt.timedelta(days=5, seconds=14400), Decimal("5000.00")]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 5
    assert df.columns is not None
    assert len(df.columns) == 5
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 5)

    df.to_qvd(str(tmp_path / "written.qvd"))

    assert os.path.exists(str(tmp_path / "written.qvd"))
    assert os.path.getsize(str(tmp_path / "written.qvd")) > 0

    written_df = QvdTable.from_qvd(str(tmp_path / "written.qvd"))

    assert written_df is not None
    assert written_df.shape is not None
    assert written_df.shape[0] == 5
    assert written_df.shape[1] == 5

    written_columns = written_df.to_dict()["columns"]
    written_data = written_df.to_dict()["data"]

    assert written_columns == ["Key", "Value", "Timestamp", "Duration", "Salary"]
    assert written_data[0] == [1, "A", dt.datetime(2021, 1, 1, 0, 0, 0),
                               dt.timedelta(days=1, seconds=3620), Decimal("1000.00")]
    assert written_data[1] == [2, "B", dt.datetime(2021, 1, 2, 0, 0, 0),
                               dt.timedelta(days=2, seconds=7240), Decimal("2000.00")]
    assert written_data[2] == [3, "C", dt.datetime(2021, 1, 3, 0, 0, 0),
                               dt.timedelta(days=3, seconds=7200), Decimal("3000.00")]
    assert written_data[3] == [4, "D", dt.datetime(2021, 1, 4, 0, 0, 0),
                               dt.timedelta(days=4, seconds=10800), Decimal("4000.00")]
    assert written_data[4] == [5, "E", dt.datetime(2021, 1, 5, 0, 0, 0),
                               dt.timedelta(days=5, seconds=14400), Decimal("5000.00")]

def test_write_qvd_file_as_binary_file_stream(tmp_path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to a binary stream successfully.
    """
    raw_df = {
        "columns": ["Key", "Value", "Timestamp"],
        "data": [
            [1, "A", dt.datetime(2021, 1, 1, 0, 0, 0)],
            [2, "B", dt.datetime(2021, 1, 2, 0, 0, 0)],
            [3, "C", dt.datetime(2021, 1, 3, 0, 0, 0)],
            [4, "D", dt.datetime(2021, 1, 4, 0, 0, 0)],
            [5, "E", dt.datetime(2021, 1, 5, 0, 0, 0)]
        ]
    }

    df = QvdTable.from_dict(raw_df)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 5
    assert df.shape[1] == 3
    assert df.columns is not None
    assert len(df.columns) == 3
    assert df.data is not None
    assert len(df.data) == 5
    assert df.head(2).shape == (2, 3)

    with open(str(tmp_path / "written.qvd"), "wb") as file:
        df.to_stream(file)

    assert os.path.exists(tmp_path / "written.qvd")
    assert os.path.getsize(tmp_path / "written.qvd") > 0

    written_df = QvdTable.from_qvd(str(tmp_path / "written.qvd"))

    assert written_df is not None
    assert written_df.shape is not None
    assert written_df.shape[0] == 5
    assert written_df.shape[1] == 3

    written_columns = written_df.to_dict()["columns"]
    written_data = written_df.to_dict()["data"]

    assert written_columns == ["Key", "Value", "Timestamp"]
    assert written_data[0] == [1, "A", dt.datetime(2021, 1, 1, 0, 0, 0)]
    assert written_data[1] == [2, "B", dt.datetime(2021, 1, 2, 0, 0, 0)]
    assert written_data[2] == [3, "C", dt.datetime(2021, 1, 3, 0, 0, 0)]
    assert written_data[3] == [4, "D", dt.datetime(2021, 1, 4, 0, 0, 0)]
    assert written_data[4] == [5, "E", dt.datetime(2021, 1, 5, 0, 0, 0)]
