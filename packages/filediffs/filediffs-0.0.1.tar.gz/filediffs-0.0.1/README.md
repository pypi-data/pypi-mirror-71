# The filediffs package
`filediffs` takes two files and separates them into 
1. lines found in both files
2. lines found only in file 1
3. lines found only in file 2

Code inspired by https://www.splinter.com.au/reconcilingcomparing-huge-data-sets-with-c/

# Installation
For package installation, [Poetry](https://python-poetry.org/) is used.

Inside pyproject.toml the python version, requirements,
build instructions, package descriptions etc. are defined.

You can create a virtual environment for the package with
poetry by 
1. installing poetry `pip install poetry`
2. calling `poetry install` to install from poetry.lock

To create a .tar.gz file and wheeles for publishing the package one can use `poetry build`

To publish the package, `poetry publish` can be used. Though 
the pipy credentials have to be set (see https://python-poetry.org/docs/repositories/#configuring-credentials).

# Implementation:
Implemented in Cython.

Lines found in both files are not kept in memory but written to
 disk every 5.000.000 lines to preserve memory. 
 
This way, even very large files can be separated.
Only the diff has to fit in memory.

The file `build_cython_setup.py` defines the cython build process.
 The cpp files can be build using `python build_cython_setup.py build_ext --inplace`.
 
 # Usage:
To use the method in python in interaction with cython,
the file paths have to passed to the function as bytestrings.
```python
from filediffs.filediffs import file_diffs
lines_only_in_file_1, lines_only_in_file_2 = file_diffs(
    filename_1=b'path/to/file1.txt',
    filename_2=b'path/to/file2.txt',
    outpath_lines_present_in_both_files=b'output_path/to/lines_in_both.txt',
    outpath_lines_present_only_in_file1=b'output_path/to/lines_only_in_file1.txt',
    outpath_lines_present_only_in_file2=b'output_path/to/lines_only_in_file2.txt',
)
```

Inside the package directory, an example script `filediffs_script.py` is provided.

It can be used to separate files from the terminal:
```
# To separate two files, simply pass the filepath to `filediffs/filediffs_script.py`
python filediffs/filediffs_script.py filediffs/tests/data/file_1.txt filediffs/tests/data/file_2.txt

# If you want to define the filenames of the separated files, optional arguments are provided for the script. 
python filediffs/filediffs_script.py filediffs/tests/data/file_1.txt filediffs/tests/data/file_2.txt --out_filename_both out_both.txt --out_filename_only_in_file1 out_file1_only.txt --out_filename_only_in_file2 out_file2_only.txt
```


