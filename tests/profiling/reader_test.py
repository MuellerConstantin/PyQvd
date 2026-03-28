"""
This module contains tests for profiling the QvdFileReader.
"""

import os
from pathlib import Path
import pytest
from pyinstrument import Profiler
from pyqvd.io.reader import QvdFileReader

@pytest.mark.profiling
def test_profile_read(test_data_dir: Path):
    """
    Profile the reading of a QVD file.
    """
    file_path = test_data_dir / "huge.qvd"

    profiler = Profiler()
    profiler.start()

    table = QvdFileReader(file_path).read()

    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))

    os.makedirs(".profiling", exist_ok=True)
    profiler.write_html(".profiling/reader_test.html")

    assert table is not None
