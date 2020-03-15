#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Uncompress program for tar, tar.gz, zip, etc

Args:
    - Path to the compressed file to extract
    - Path to the output folder for extracted files

Example:
    python3 uncompress.py -i path/to/file.tar.gz -o path/for/extractedfiles
"""

import argparse
import shutil


def extract(compressedfile, extract_path):
    '''Extract files

    Args:
        - compressedfile    (str) : path to the compressed file
        - extract_path      (str) : path for the extracted files
    '''
    shutil.unpack_archive(compressedfile, extract_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--compressedfile",
        required=True,
        type=str,
        help="Path to the file to uncompress."
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=str,
        help="Output path for the extracted files."
    )

    args = parser.parse_args()

    extract(args.compressedfile, args.output)


if __name__ == '__main__':
    main()
