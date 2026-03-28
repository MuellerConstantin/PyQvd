"""
Tests the performance of writing QVD files.
"""

from pathlib import Path
import pytest
from pyqvd import QvdTable

@pytest.mark.benchmark(group="qvd-write")
@pytest.mark.parametrize(
    "file_name",
    [
        "small.qvd",
        "medium.qvd",
        "large.qvd",
        "huge.qvd",
        "giant.qvd",
    ],
)
def test_benchmark_qvd_write(benchmark, file_name: str, test_data_dir: Path, tmp_path: Path):
    """
    Benchmark writing a QVD file of different sizes.
    """
    source = test_data_dir / file_name
    table = QvdTable.from_qvd(str(source))

    file_size = source.stat().st_size / (1024 * 1024)

    def write():
        target = tmp_path / f"out_{file_name}"
        table.to_qvd(str(target))
        target.unlink()

    benchmark(write)

    benchmark.extra_info.update({
        "input_file_size": round(file_size, 2),
        "rows": len(table.data),
        "columns": len(table.columns),
    })
