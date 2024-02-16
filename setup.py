import os
from setuptools import setup, find_packages

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(CURRENT_DIR, 'README.md')) as file:
    LONG_DESCRIPTION = file.read()

setup(
    name="PyQvd",
    version="0.1.0",
    packages=find_packages(include=["pyqvd", "pyqvd.*"]),
    include_package_data=True,
    python_requires='>=3.7',
    platforms=['OS-independent'],
    author="Constantin Müller",
    author_email="info@mueller-constantin.de",
    description="Utility library for reading Qlik View Data (QVD) files in Python.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/MuellerConstantin/PyQvd",
    keywords=['Qlik', 'QVD', 'Qlik Sense', 'Qlik View'],
    license="MIT",
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
