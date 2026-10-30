"""
Tests the functionality related to reading files.
"""

import hashlib
import io
from pathlib import Path
from typing import List, Tuple
import pytest
from pyqvd import QvdTable

class NonSeekableBytesIO(io.BytesIO):
    """Simple non-seekable stream wrapper for reader tests."""
    def seekable(self) -> bool:
        return False

    def seek(self, offset, whence=0):
        raise io.UnsupportedOperation("stream is not seekable")

def _cells(table: QvdTable) -> List[List[Tuple]]:
    """
    Returns the cells of a table as (type, calculation value, display value) tuples. QvdValue
    equality only compares calculation values, which would not detect a wrong value type.
    """
    # The public data property returns a deep copy, which is too slow for the large fixture
    rows = table._data  # pylint: disable=protected-access

    return [[None if value is None else (type(value).__name__, value.calculation_value, value.display_value)
             for value in row] for row in rows]

def _fingerprint(table: QvdTable) -> str:
    """
    Returns a hash over all cells of a table, including their types and display values.
    """
    return hashlib.sha256(repr(_cells(table)).encode()).hexdigest()

def _read_all_chunks(source, chunk_size: int) -> QvdTable:
    """
    Reads a QVD source in chunks and concatenates the chunks to a single table.
    """
    if isinstance(source, io.IOBase):
        itr = QvdTable.from_stream(source, chunk_size=chunk_size)
    else:
        itr = QvdTable.from_qvd(source, chunk_size=chunk_size)

    total_tbl = None

    for tbl in itr:
        total_tbl = tbl if total_tbl is None else total_tbl.concat(tbl)

    return total_tbl

def _build_qvd(fields: List[dict], symbol_table: bytes, index_table: bytes, record_byte_size: int,
               no_of_records: int) -> bytes:
    """
    Builds a minimal QVD file from raw parts, allowing header constellations that are not
    covered by the fixtures.
    """
    fields_xml = "".join(
        "<QvdFieldHeader>"
        f"<FieldName>{field['name']}</FieldName>"
        f"<BitOffset>{field['bit_offset']}</BitOffset>"
        f"<BitWidth>{field['bit_width']}</BitWidth>"
        f"<Bias>{field['bias']}</Bias>"
        "<NumberFormat><Type>UNKNOWN</Type><nDec>0</nDec><UseThou>0</UseThou>"
        "<Fmt></Fmt><Dec></Dec><Thou></Thou></NumberFormat>"
        f"<NoOfSymbols>{field['no_of_symbols']}</NoOfSymbols>"
        f"<Offset>{field['offset']}</Offset>"
        f"<Length>{field['length']}</Length>"
        "<Comment></Comment><Tags></Tags>"
        "</QvdFieldHeader>"
        for field in fields
    )
    header = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        "<QvdTableHeader>"
        "<QvBuildNo>50668</QvBuildNo><CreatorDoc></CreatorDoc><CreateUtcTime></CreateUtcTime>"
        "<SourceCreateUtcTime></SourceCreateUtcTime><SourceFileUtcTime></SourceFileUtcTime>"
        "<StaleUtcTime></StaleUtcTime><TableName>Test</TableName><SourceFileSize>-1</SourceFileSize>"
        f"<Fields>{fields_xml}</Fields>"
        "<Compression></Compression>"
        f"<RecordByteSize>{record_byte_size}</RecordByteSize>"
        f"<NoOfRecords>{no_of_records}</NoOfRecords>"
        f"<Offset>{len(symbol_table)}</Offset>"
        f"<Length>{len(index_table)}</Length>"
        "<Comment></Comment><Lineage></Lineage>"
        "</QvdTableHeader>\r\n"
    )

    return header.encode() + b"\0" + symbol_table + index_table

def _build_edge_case_qvd() -> bytes:
    """
    Builds a QVD file with a nullable field (bias -2), a constant field and an all-null field
    (both bit width 0) and a field whose indices span a byte boundary.
    """
    nullable_symbols = b"".join(b"\x01" + value.to_bytes(4, "little", signed=True) for value in (10, 20))
    constant_symbols = b"\x04x\0"
    wide_symbols = b"".join(b"\x01" + value.to_bytes(4, "little", signed=True) for value in range(300))

    fields = [
        {"name": "Nullable", "bit_offset": 0, "bit_width": 2, "bias": -2, "no_of_symbols": 2,
         "offset": 0, "length": len(nullable_symbols)},
        {"name": "Constant", "bit_offset": 0, "bit_width": 0, "bias": 0, "no_of_symbols": 1,
         "offset": len(nullable_symbols), "length": len(constant_symbols)},
        {"name": "AllNull", "bit_offset": 0, "bit_width": 0, "bias": -2, "no_of_symbols": 0,
         "offset": len(nullable_symbols) + len(constant_symbols), "length": 0},
        {"name": "Wide", "bit_offset": 2, "bit_width": 9, "bias": 0, "no_of_symbols": 300,
         "offset": len(nullable_symbols) + len(constant_symbols), "length": len(wide_symbols)},
    ]
    raw_records = [(0, 0), (2, 299), (3, 1), (1, 256)]
    index_table = b"".join((nullable | wide << 2).to_bytes(2, "little") for nullable, wide in raw_records)

    return _build_qvd(fields, nullable_symbols + constant_symbols + wide_symbols, index_table, 2,
                      len(raw_records))

EDGE_CASE_EXPECTED_CELLS = [
    [None, ("StringValue", "x", "x"), None, ("IntegerValue", 0, "0")],
    [("IntegerValue", 10, "10"), ("StringValue", "x", "x"), None, ("IntegerValue", 299, "299")],
    [("IntegerValue", 20, "20"), ("StringValue", "x", "x"), None, ("IntegerValue", 1, "1")],
    [None, ("StringValue", "x", "x"), None, ("IntegerValue", 256, "256")],
]

def test_read_qvd_file_with_1000_rows(test_data_dir: Path):
    """
    Tests if a small QVD file can be parsed properly.
    """
    df = QvdTable.from_qvd(test_data_dir / "small.qvd")

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 1000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 1000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_with_20000_rows(test_data_dir: Path):
    """
    Tests if a medium QVD file can be parsed properly.
    """
    df = QvdTable.from_qvd(test_data_dir / "medium.qvd")

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 20000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 20000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_with_60000_rows(test_data_dir: Path):
    """
    Tests if a large QVD file can be parsed properly.
    """
    df = QvdTable.from_qvd(test_data_dir / "large.qvd")

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 200000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 200000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_in_chunks(test_data_dir: Path):
    """
    Tests if a large QVD file can be parsed properly in chunks.
    """
    itr = QvdTable.from_qvd(test_data_dir / "medium.qvd", chunk_size=5000)

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

def test_read_damaged_qvd_file(test_data_dir: Path):
    """
    Tests if reading a damaged QVD file fails as expected.
    """
    with pytest.raises(Exception):
        QvdTable.from_qvd(test_data_dir / "damaged.qvd")

def test_read_binary_file_stream_in_chunks(test_data_dir: Path):
    """
    Tests if QVD table can be read from a binary file stream properly in chunks.
    """
    with open(test_data_dir / "medium.qvd", "rb") as file:
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

def test_read_binary_file_stream(test_data_dir: Path):
    """
    Tests if QVD table can be read from a binary file stream properly.
    """
    with open(test_data_dir / "small.qvd", "rb") as file:
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


def test_read_non_seekable_binary_file_stream_in_chunks(test_data_dir: Path):
    """
    Tests if QVD table can be read in chunks from a non-seekable binary stream.
    """
    with open(test_data_dir / "medium.qvd", "rb") as file:
        stream = NonSeekableBytesIO(file.read())
        itr = QvdTable.from_stream(stream, chunk_size=5000)

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


def test_read_non_seekable_binary_file_stream(test_data_dir: Path):
    """
    Tests if QVD table can be read from a non-seekable binary stream.
    """
    with open(test_data_dir / "small.qvd", "rb") as file:
        stream = NonSeekableBytesIO(file.read())
        df = QvdTable.from_stream(stream)

    assert df is not None
    assert df.shape is not None
    assert df.shape[0] == 1000
    assert df.shape[1] == 6
    assert df.columns is not None
    assert len(df.columns) == 6
    assert df.data is not None
    assert len(df.data) == 1000
    assert df.head(5).shape == (5, 6)

def test_read_qvd_file_with_pathlib(test_data_dir: Path):
    """
    Tests if QVD table can be read from a pathlib Path object properly.
    """
    path = test_data_dir / "small.qvd"
    df = QvdTable.from_qvd(path)

    assert df is not None

@pytest.mark.parametrize(
    "file_name, fingerprint, first_row, last_row",
    [
        (
            "small.qvd",
            "aee1ca86dc4a2e2d0983f53ce2eb52ebfa4c5dcc4a4ec0c4e6d01c993a61b776",
            [("IntegerValue", 1, "1"), ("StringValue", "Delta", "Delta"),
             ("DateValue", 44428, "20.08.2021"), ("DoubleValue", 3106.33, "3106.33"),
             ("StringValue", "Open", "Open"), ("DualIntegerValue", 0, "0")],
            [("IntegerValue", 1000, "1000"), ("StringValue", "Delta", "Delta"),
             ("DateValue", 43906, "16.03.2020"), ("DoubleValue", 7799.4800000000005, "7799.4800000000005"),
             ("StringValue", "Open", "Open"), ("DualIntegerValue", 0, "0")],
        ),
        (
            "medium.qvd",
            "1719971c6899b827ba8714b3b25df8a3611061bd57d138d6d64264d5469468b8",
            [("IntegerValue", 1, "1"), ("StringValue", "Delta", "Delta"),
             ("DateValue", 44049, "06.08.2020"), ("DoubleValue", 1612.3, "1612.3"),
             ("StringValue", "Open", "Open"), ("DualIntegerValue", 0, "0")],
            [("IntegerValue", 20000, "20000"), ("StringValue", "Gamma", "Gamma"),
             ("DateValue", 44747, "05.07.2022"), ("DoubleValue", 9606.86, "9606.86"),
             ("StringValue", "Completed", "Completed"), ("DualIntegerValue", 1, "1")],
        ),
        (
            "large.qvd",
            "ecaf889e93f57a845d4715015d5d49e686d3cc0fcc05bf9c66ad4a3cb235220d",
            [("IntegerValue", 1, "1"), ("StringValue", "Alpha", "Alpha"),
             ("DateValue", 43978, "27.05.2020"), ("DoubleValue", 8941.84, "8941.84"),
             ("StringValue", "Completed", "Completed"), ("DualIntegerValue", 1, "1")],
            [("IntegerValue", 200000, "200000"), ("StringValue", "Alpha", "Alpha"),
             ("DateValue", 43854, "24.01.2020"), ("DoubleValue", 9720.19, "9720.19"),
             ("StringValue", "Open", "Open"), ("DualIntegerValue", 0, "0")],
        ),
    ],
)
def test_read_qvd_file_values(test_data_dir: Path, file_name: str, fingerprint: str,
                              first_row: List[Tuple], last_row: List[Tuple]):
    """
    Tests if every cell of a QVD file is decoded to the correct value, type and display value.
    """
    df = QvdTable.from_qvd(test_data_dir / file_name)
    cells = _cells(df)

    assert cells[0] == first_row
    assert cells[-1] == last_row
    assert _fingerprint(df) == fingerprint

@pytest.mark.parametrize("chunk_size", [5000, 3333, 1])
def test_read_qvd_file_in_chunks_matches_full_read(test_data_dir: Path, chunk_size: int):
    """
    Tests if reading a QVD file in chunks yields exactly the same cells as reading it at once,
    including a partially filled last chunk.
    """
    path = test_data_dir / ("small.qvd" if chunk_size == 1 else "medium.qvd")

    assert _cells(_read_all_chunks(path, chunk_size)) == _cells(QvdTable.from_qvd(path))

def test_read_qvd_file_with_nulls_and_zero_bit_width():
    """
    Tests if null values (negative indices after applying the bias), fields with a bit width of
    zero and indices spanning a byte boundary are decoded correctly.
    """
    data = _build_edge_case_qvd()
    df = QvdTable.from_stream(io.BytesIO(data))

    assert df.columns == ["Nullable", "Constant", "AllNull", "Wide"]
    assert _cells(df) == EDGE_CASE_EXPECTED_CELLS

def test_read_qvd_file_with_nulls_and_zero_bit_width_in_chunks():
    """
    Tests if null values and fields with a bit width of zero are decoded correctly when reading
    in chunks.
    """
    data = _build_edge_case_qvd()

    assert _cells(_read_all_chunks(io.BytesIO(data), 3)) == EDGE_CASE_EXPECTED_CELLS

def test_read_written_qvd_file_with_nulls():
    """
    Tests if null values survive a write and read round trip.
    """
    df = QvdTable.from_dict({
        "columns": ["A", "B"],
        "data": [[1, None], [None, "x"], [2, "y"], [None, None]],
    })
    stream = io.BytesIO()
    df.to_stream(stream)
    stream.seek(0)

    assert _cells(QvdTable.from_stream(stream)) == _cells(df)
