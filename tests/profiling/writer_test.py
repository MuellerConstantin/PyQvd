"""
This module contains tests for profiling the QvdFileReader.
"""

import os
from pathlib import Path
import pytest
from pyinstrument import Profiler
from pyqvd.io.reader import QvdFileReader
from pyqvd.io.writer import QvdFileWriter

@pytest.mark.profiling
def test_profile_write(tmp_path: Path, test_data_dir: Path):
    """
    Profile the writing of a QVD file.
    """
    source = test_data_dir / "huge.qvd"
    target = tmp_path / "write_profile.qvd"

    table = QvdFileReader(source).read()

    profiler = Profiler()
    profiler.start()

    QvdFileWriter(target, table).write()

    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))

    os.makedirs(".profiling", exist_ok=True)
    profiler.write_html(".profiling/writer_test.html")

    assert target.exists()
