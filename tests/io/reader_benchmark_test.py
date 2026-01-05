"""
Tests the performance of reading QVD files.
"""

from pathlib import Path
import pytest
from pyqvd import QvdTable

DATA_DIR = Path(__file__).parent / ".." / "data"

@pytest.mark.benchmark(group="qvd-read")
@pytest.mark.parametrize(
    "file_name",
    [
        "small.qvd",    # ~1k rows
        "medium.qvd",   # ~20k rows
        "large.qvd",    # ~200k rows
        "huge.qvd",     # ~2M rows
    ],
)
def test_benchmark_qvd_read(benchmark, file_name):
    """
    Benchmark reading a QVD file of different sizes.
    """
    path = DATA_DIR / file_name
    file_size = path.stat().st_size / (1024 * 1024)

    table = benchmark(QvdTable.from_qvd, str(path))

    benchmark.extra_info.update({
        "file_size": round(file_size, 2),
        "rows": len(table.data),
        "columns": len(table.columns),
    })
