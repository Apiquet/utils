#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF manager:
    - remove pages (TODO)
    - change pages order (TODO)
    - compress pdf
    - add signature to pages (TODO)

Args:
    - Path to the pdf file
    - Option wanted
    - List of pages concerned

Example:
    - compression
    install GhostScript from https://www.ghostscript.com/download/gsdnld.html
    then run:
    python pages_manager.py -i input.pdf -o output.pdf\
        -w compress -g path/to/gswin64c.exe
"""

import argparse
import os
from PyPDF2 import PdfFileWriter, PdfFileReader


def compress_pdf(pdf_file, output_path, power_compression, gs_path):
    '''Extract files

    Args:
        - compressedfile    (str) : path to the compressed file
        - extract_path      (str) : path for the extracted files
    '''
    dict_compression_power = {
            1: "/default",
            2: "/printer",
            3: "/prepress",
            4: "/ebook",
            5: "/screen"}
    level_of_compression = dict_compression_power[power_compression]

    os.system(gs_path +
              " -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 " +
              "-dPDFSETTINGS=" + level_of_compression +
              " -dNOPAUSE -dQUIET -dBATCH -sOutputFile=" +
              output_path + " " + pdf_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_pdf",
        required=True,
        type=str,
        help="Path to the pdf file."
    )
    parser.add_argument(
        "-o",
        "--output_pdf",
        required=True,
        type=str,
        help="Path to the pdf file."
    )
    parser.add_argument(
        "-w",
        "--wishto",
        required=True,
        choices=['removeTODO', 'keepTODO', 'compress', 'changeorderTODO'],
        type=str,
        help="Option wanted."
    )
    parser.add_argument(
        "-g",
        "--gs_path",
        required=False,
        default=None,
        type=str,
        help="path/to/gswin64c.exe"
    )
    parser.add_argument(
        "-p",
        "--power_compression",
        required=False,
        choices=[1, 2, 3, 4, 5],
        default=4,
        type=int,
        help="compression power from 1 to 5"
    )
    parser.add_argument(
        "-l",
        "--list_of_pages",
        required=False,
        type=list,
        help="List of pages concerned."
    )

    args = parser.parse_args()

    if args.wishto == "compress":
        assert args.gs_path is not None,\
               "You should specify GhostScript path to compress pdf file"
        compress_pdf(args.input_pdf, args.output_pdf,
                     args.power_compression, args.gs_path)        


if __name__ == '__main__':
    main()
