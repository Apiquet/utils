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
import os
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        type=str,
        help="Path to a folder to binarize with '//'\
            or a binary file to extract."
    )
    parser.add_argument(
        "-o",
        "--output_name",
        required=False,
        default=None,
        type=str,
        help="Name of the output binary or folder, default:\
            If binarize mode: take the input folder name,\
            If extract mode: take the binary name"
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        required=False,
        default="delimiter",
        type=str,
        help="Delimiter to use"
    )

    args = parser.parse_args()

    # if input is directory: encode files to a .bin file
    if os.path.isdir(args.input_path):
        files_path = glob(args.input_path + '/*')
        binary = b''

        for file_path in tqdm(files_path):
            # write file name
            binary += os.path.basename(file_path).encode()
            binary += args.delimiter.encode()

            # write content
            file = open(file_path, "rb")
            binary += file.read()
            binary += args.delimiter.encode()

        if args.output_name is None:
            bin_name = os.path.basename(args.input_path).split('.')[0]
        else:
            bin_name = args.output_name
        result = open(args.input_path + '/' + bin_name, "wb")
        result.write(binary)
        result.close()
    # if input is .bin file: extract all files from it
    else:
        if args.output_name is None:
            bin_name = os.path.basename(args.input_path).split('.')[0]
        else:
            bin_name = args.output_name
        output_path = os.path.dirname(args.input_path) + '/' + bin_name + '/'
        os.makedirs(output_path)

        file = open(args.input_path, "rb")
        elements = list(filter(None, file.read().split(
            args.delimiter.encode())))
        file.close()
        print(len(elements))
        elements_name = "wrong_name"

        for i, el in tqdm(enumerate(elements)):
            if i%2 == 0:
                element_name = el.decode()
            else:
                file = open(output_path + element_name, "wb")
                file.write(el)
                file.close()


if __name__ == '__main__':
    main()
