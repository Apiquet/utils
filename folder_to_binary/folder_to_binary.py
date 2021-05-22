#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Folder to binary

- Convert a folder of files to a simple .bin file
- extract the .bin file to get the folder

Args:
    - Path to the folder
    - name for the .bin file (default is folder_name.bin)

Example:

    binarize folder:
    python folder_to_binary.py -i myfolder/
    will create myfolder.bin with all files

    extract .bin file:
    python folder_to_binary.py -i mybin.bin
    will create mybin.bin to mybin/ with all files
"""

import argparse
from glob import glob

from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        type=str,
        help="Path to a folder."
    )
    parser.add_argument(
        "-o",
        "--output_name",
        required=False,
        default=None,
        type=str,
        help="Name of the output .bin file (default is the input folder name)"
    )

    args = parser.parse_args()


if __name__ == '__main__':
    main()
