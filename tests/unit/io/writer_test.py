"""
Tests the functionality related to persisting files.
"""

import hashlib
import io
import os
import re
from pathlib import Path
import datetime as dt
from decimal import Decimal
from typing import List, Tuple
import xml.etree.ElementTree as ET
import pytest
from pyqvd import (QvdTable, DateValue, IntegerValue, DoubleValue, StringValue, DualIntegerValue, TimeValue,
                   TimestampValue, IntervalValue, MoneyValue)
from pyqvd.io import QvdFileWriter, QvdFileWriterOptions, DateValueFormatter

def test_write_qvd_file(tmp_path: Path):
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

def test_write_qvd_file_custom_options(tmp_path: Path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to file successfully with custom options.
    """
    raw_df = {
        "columns": ["Key", "Value", "Date"],
        "data": [
            [1, "A", dt.datetime(2021, 1, 1).date()],
            [2, "B", dt.datetime(2021, 1, 2).date()],
            [3, "C", dt.datetime(2021, 1, 3).date()],
            [4, "D", dt.datetime(2021, 1, 4).date()],
            [5, "E", dt.datetime(2021, 1, 5).date()]
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

    options = QvdFileWriterOptions()
    options.date_formatter = DateValueFormatter("DD.MM.YYYY")

    writer = QvdFileWriter(str(tmp_path / "written.qvd"), df, options)
    writer.write()

    assert os.path.exists(str(tmp_path / "written.qvd"))
    assert os.path.getsize(str(tmp_path / "written.qvd")) > 0

    written_df = QvdTable.from_qvd(str(tmp_path / "written.qvd"))

    assert written_df is not None
    assert written_df.shape is not None
    assert written_df.shape[0] == 5
    assert written_df.shape[1] == 3

    written_columns = written_df.to_dict()["columns"]
    written_data = written_df.to_dict()["data"]

    assert written_columns == ["Key", "Value", "Date"]
    assert written_data[0] == [1, "A", dt.datetime(2021, 1, 1).date()]
    assert written_data[1] == [2, "B", dt.datetime(2021, 1, 2).date()]
    assert written_data[2] == [3, "C", dt.datetime(2021, 1, 3).date()]
    assert written_data[3] == [4, "D", dt.datetime(2021, 1, 4).date()]
    assert written_data[4] == [5, "E", dt.datetime(2021, 1, 5).date()]

    assert isinstance(written_df.data[0][2], DateValue)
    assert written_df.data[0][2].display_value == "01.01.2021"
    assert isinstance(written_df.data[1][2], DateValue)
    assert written_df.data[1][2].display_value == "02.01.2021"
    assert isinstance(written_df.data[2][2], DateValue)
    assert written_df.data[2][2].display_value == "03.01.2021"
    assert isinstance(written_df.data[3][2], DateValue)
    assert written_df.data[3][2].display_value == "04.01.2021"
    assert isinstance(written_df.data[4][2], DateValue)
    assert written_df.data[4][2].display_value == "05.01.2021"

def test_write_qvd_file_none_options(tmp_path: Path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to file successfully with None options.
    """
    raw_df = {
        "columns": ["Key", "Value", "Date"],
        "data": [
            [1, "A", dt.datetime(2021, 1, 1).date()],
            [2, "B", dt.datetime(2021, 1, 2).date()],
            [3, "C", dt.datetime(2021, 1, 3).date()],
            [4, "D", dt.datetime(2021, 1, 4).date()],
            [5, "E", dt.datetime(2021, 1, 5).date()]
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

    writer = QvdFileWriter(str(tmp_path / "written.qvd"), df, None)
    writer.write()

    assert os.path.exists(str(tmp_path / "written.qvd"))
    assert os.path.getsize(str(tmp_path / "written.qvd")) > 0

    written_df = QvdTable.from_qvd(str(tmp_path / "written.qvd"))

    assert written_df is not None
    assert written_df.shape is not None
    assert written_df.shape[0] == 5
    assert written_df.shape[1] == 3

    written_columns = written_df.to_dict()["columns"]
    written_data = written_df.to_dict()["data"]

    assert written_columns == ["Key", "Value", "Date"]
    assert written_data[0] == [1, "A", dt.datetime(2021, 1, 1).date()]
    assert written_data[1] == [2, "B", dt.datetime(2021, 1, 2).date()]
    assert written_data[2] == [3, "C", dt.datetime(2021, 1, 3).date()]
    assert written_data[3] == [4, "D", dt.datetime(2021, 1, 4).date()]
    assert written_data[4] == [5, "E", dt.datetime(2021, 1, 5).date()]

def test_write_qvd_file_as_binary_file_stream(tmp_path: Path):
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

def test_write_qvd_file_with_pathlib(tmp_path: Path):
    """
    Test if a data frame, constructed from a dictionary, can be
    written to a pathlib path successfully.
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

    path = tmp_path / "written.qvd"
    df.to_qvd(path)

    assert os.path.exists(path)
    assert os.path.getsize(path) > 0

def _write_normalized(table: QvdTable) -> bytes:
    """
    Writes a table to bytes and replaces the parts of the header that differ on every write, the
    creator document id and the creation time, with fixed values.
    """
    stream = io.BytesIO()
    table.to_stream(stream)
    data = stream.getvalue()

    data = re.sub(rb"<CreatorDoc>[^<]*</CreatorDoc>", b"<CreatorDoc>x</CreatorDoc>", data, count=1)
    data = re.sub(rb"<CreateUtcTime>[^<]*</CreateUtcTime>", b"<CreateUtcTime>x</CreateUtcTime>", data, count=1)

    return data

def _written_fields(data: bytes) -> List[Tuple]:
    """
    Returns the bit layout and symbol information of every field of a written QVD file.
    """
    header = ET.fromstring(data[:data.index(b"</QvdTableHeader>") + len(b"</QvdTableHeader>")])

    return [(field.find("FieldName").text, int(field.find("BitOffset").text), int(field.find("BitWidth").text),
             int(field.find("Bias").text), int(field.find("NoOfSymbols").text))
            for field in header.find("Fields")]

@pytest.mark.parametrize(
    "file_name, fingerprint",
    [
        ("small.qvd", "1bf904774edac016566aaaa28ff760384c133fa52db96c21e7219e0b370f8a17"),
        ("medium.qvd", "19afb5c7225fb5000a35a7690a7b4c727c82c50e4a9c0a76ac3fade486f8d5bf"),
        ("large.qvd", "e0b149274eed40e2d50d39867b1de3b7aecaacb6c150992920e7b6d6f71ec1d3"),
    ],
)
def test_write_qvd_file_bytes(test_data_dir: Path, file_name: str, fingerprint: str):
    """
    Tests if writing the fixtures yields exactly the same bytes, guarding header, symbol table and
    index table against unnoticed changes.
    """
    df = QvdTable.from_qvd(test_data_dir / file_name)

    assert hashlib.sha256(_write_normalized(df)).hexdigest() == fingerprint

def _build_edge_case_table() -> QvdTable:
    """
    Builds a table with null values, a constant column, a column whose indices need more than a
    byte, so records span multiple bytes, and a column for every value type.
    """
    mixed = [IntegerValue(1), DoubleValue(2.5), StringValue("txt"), DualIntegerValue(3, "drei"), None]
    data = [
        [
            None if i % 3 == 0 else IntegerValue(i % 5),
            StringValue("x"),
            IntegerValue(i),
            mixed[i % len(mixed)],
            DateValue.from_date(dt.date(2021, 1, 1) + dt.timedelta(days=i % 7)),
            TimeValue.from_time(dt.time(i % 24, i % 60, 0, 250000)),
            TimestampValue.from_timestamp(dt.datetime(2021, 3, 7, 14, 5, 9, 123000) + dt.timedelta(hours=i % 4)),
            IntervalValue.from_interval(dt.timedelta(minutes=i % 3, milliseconds=5)),
            MoneyValue.from_money(Decimal("1234.50") + i % 2),
        ]
        for i in range(300)
    ]
    columns = ["Nullable", "Constant", "Wide", "Mixed", "Date", "Time", "Timestamp", "Interval", "Money"]

    return QvdTable(data, columns)

def test_write_qvd_file_bytes_with_edge_cases():
    """
    Tests if null values, constant columns, multi-byte records and all value types are written
    with the expected bit layout and exactly the same bytes.
    """
    data = _write_normalized(_build_edge_case_table())

    assert _written_fields(data) == [
        ("Nullable", 0, 3, -2, 5),
        ("Constant", 3, 1, 0, 1),
        ("Wide", 4, 9, 0, 300),
        ("Mixed", 13, 3, -2, 4),
        ("Date", 16, 3, 0, 7),
        ("Time", 19, 7, 0, 120),
        ("Timestamp", 26, 2, 0, 4),
        ("Interval", 28, 2, 0, 3),
        ("Money", 30, 1, 0, 2),
    ]
    assert hashlib.sha256(data).hexdigest() == "584e79dd2eecc029013880c0659e4e57415fe35e3c4f84d9e841bf2e54283803"

def test_write_qvd_file_round_trip_with_edge_cases():
    """
    Tests if null values, constant columns, multi-byte records and all value types survive a
    write and read round trip.
    """
    df = _build_edge_case_table()
    stream = io.BytesIO()
    df.to_stream(stream)
    stream.seek(0)
    written_df = QvdTable.from_stream(stream)

    # pylint: disable-next=protected-access
    for expected_row, written_row in zip(df._data, written_df._data):
        assert [None if v is None else (type(v), v.calculation_value) for v in written_row] == \
            [None if v is None else (type(v), v.calculation_value) for v in expected_row]
