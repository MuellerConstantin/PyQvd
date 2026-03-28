"""
Tests the performance of reading QVD files.
"""

from pathlib import Path
import pytest
from pyqvd import QvdTable

@pytest.mark.benchmark(group="qvd-read")
@pytest.mark.parametrize(
    "file_name",
    [
        "small.qvd",    # ~1k rows 6 columns
        "medium.qvd",   # ~20k rows 6 columns
        "large.qvd",    # ~200k rows 6 columns
        "huge.qvd",     # ~2M rows 6 columns
        "giant.qvd",    # ~20M rows 6 columns
    ],
)
def test_benchmark_qvd_read(benchmark, file_name: str, test_data_dir: Path):
    """
    Benchmark reading a QVD file of different sizes.
    """
    path = test_data_dir / file_name
    file_size = path.stat().st_size / (1024 * 1024)

    table = benchmark(QvdTable.from_qvd, str(path))

    benchmark.extra_info.update({
        "file_size": round(file_size, 2),
        "rows": len(table.data),
        "columns": len(table.columns),
    })
