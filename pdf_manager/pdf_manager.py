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
    - compression:
    install GhostScript from https://www.ghostscript.com/download/gsdnld.html
    then run:
    python pdf_manager.py -i input.pdf -o output.pdf\
        -w compress -g path/to/gswin64c.exe

    - keep some pages:
    To keep the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -l 2,3,4 -w keep

    - remove some pages:
    To remove the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -l 2,3,4 -w remove
"""

import argparse
import os
from PyPDF2 import PdfFileWriter, PdfFileReader


def compress_pdf(pdf_file, output_path, power_compression, gs_path):
    '''Compress pdf file at different levels 1 to 5

    Args:
        - pdf_file          (str): path to the pdf file
        - output_path       (str): path for output pdf file
        - power_compression (int): level of compression from 1 to 5
        - gs_path           (str): path to gswin64c.exe
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


def remove_pages(pdf_file, output_path, list_of_pages):
    '''Remove pages from pdf file

    Args:
        - pdf_file       (str): path to the pdf file
        - output_path    (str): path to the output pdf file
        - list_of_pages  (list of int): pages to remove
    '''
    infile = PdfFileReader(pdf_file, 'rb')
    output = PdfFileWriter()

    for i in range(infile.getNumPages()):
        if i not in list_of_pages:
            p = infile.getPage(i)
            output.addPage(p)

    with open(output_path, 'wb') as f:
        output.write(f)


def keep_pages(pdf_file, output_path, list_of_pages):
    '''Keep pages from pdf file

    Args:
        - pdf_file       (str): path to the pdf file
        - output_path    (str): path to the output pdf file
        - list_of_pages  (list of int): pages to remove
    '''
    infile = PdfFileReader(pdf_file, 'rb')
    output = PdfFileWriter()

    for i in list_of_pages:
        p = infile.getPage(i)
        output.addPage(p)

    with open(output_path, 'wb') as f:
        output.write(f)


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
        choices=['remove', 'keep', 'compress', 'changeorder'],
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
        type=str,
        help="List of pages concerned: 1,2,5,11"
    )

    args = parser.parse_args()

    if args.wishto == "compress":
        assert args.gs_path is not None,\
               "You should specify GhostScript path to compress pdf file"
        compress_pdf(args.input_pdf, args.output_pdf,
                     args.power_compression, args.gs_path)
    elif args.wishto == "remove":
        list_of_pages = [int(p) for p in args.list_of_pages.split(',')]
        remove_pages(args.input_pdf, args.output_pdf, list_of_pages)
    elif args.wishto == "keep":
        list_of_pages = [int(p) for p in args.list_of_pages.split(',')]
        keep_pages(args.input_pdf, args.output_pdf, list_of_pages)
    elif args.wishto == "changeorder":
        remove_pages()


if __name__ == '__main__':
    main()
