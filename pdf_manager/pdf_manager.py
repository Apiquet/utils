#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF manager:
    - remove pages
    - change pages order
    - compress pdf
    - overlay each pdf page with a one page pdf
      (useful to add a signature at specific pages
      or to put "confidential" on all pages)
    - merge several pdf files

Args:
    - Path to the pdf file(s)
    - Option wanted
    - List of pages concerned

Example:
    - compression:
    install GhostScript from https://www.ghostscript.com/download/gsdnld.html
    then run:
    python pdf_manager.py -i input.pdf -o output.pdf\
        -w compress -g path/to/gswin64c.exe
    optional: -c can be add to set the power compression from 1 to 5

    - keep some pages:
    To keep the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,3,4 -w keep

    - remove some pages:
    To remove the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,3,4 -w remove

    - change pages order:
    To change to page order to page 3 then 2 then 1, run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,1,0 -w changeorder

    - merge one page pdf on specified pages or all:
    To the one page pdf with pages 2, 3 and 4 run:
    python pdf_manager.py -i test.pdf -o outputremove.pdf -w overlay
        -m overlay.pdf -p 1,2,3
"""

import argparse
import os
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger


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


def change_order(pdf_file, output_path, new_indexes):
    '''Change order of pages of pdf file

    Args:
        - pdf_file       (str): path to the pdf file
        - output_path    (str): path to the output pdf file
        - new_indexes    (list of int): list of indexes
        new_indexes=[2,1,0] to change the pages order to
        page 3, then 2, then 1
    '''
    infile = PdfFileReader(pdf_file, 'rb')
    output = PdfFileWriter()

    for i in new_indexes:
        p = infile.getPage(i)
        output.addPage(p)

    with open(output_path, 'wb') as f:
        output.write(f)


def overlay_pdf_files(pdf_file, output_path, path_overlay, pages):
    '''overlay specified pages with a one page pdf

    Args:
        - pdf_file        (str): path to the pdf file
        - output_path     (str): path to the output pdf file
        - path_overlay    (str): path to one page pdf to overlay
        - pages           (str): number of pages concerned separated by comma
    '''
    with open(pdf_file, "rb") as inFile, open(path_overlay, "rb") as overlay:
            original = PdfFileReader(inFile)
            foreground = PdfFileReader(overlay).getPage(0)

            # add all pages to a writer
            writer = PdfFileWriter()

            # merge on pages specified (on all if not specified)
            if pages is None:
                pages_to_merge = range(original.getNumPages())
            else:
                pages_to_merge = [int(p) for p in pages.split(',')]

            for i in range(original.getNumPages()):
                background = original.getPage(i)
                if i in pages_to_merge:
                    # merge the first two pages
                    background.mergePage(foreground)
                writer.addPage(background)

            # write everything in the writer to a file
            with open(output_path, "wb") as outFile:
                writer.write(outFile)


def merge_pdf_files(pdf_file, output_path):
    '''overlay specified pages with a one page pdf

    Args:
        - pdf_file        (str): path to the pdf files separated by a comma
        - output_path     (str): path to the output pdf file
    '''
    pdf_files = pdf_file.split(',')
    merger = PdfFileMerger()

    for pdf_file_path in pdf_files:
        merger.append(pdf_file_path)

    merger.write(output_path)
    merger.close()


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
        choices=['remove', 'keep', 'compress',
                 'changeorder', 'overlay', 'merge'],
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
        "-c",
        "--power_compression",
        required=False,
        choices=[1, 2, 3, 4, 5],
        default=4,
        type=int,
        help="compression power from 1 to 5"
    )
    parser.add_argument(
        "-p",
        "--pages",
        required=False,
        type=str,
        help="List of pages concerned: 1,2,5,11"
    )
    parser.add_argument(
        "-m",
        "--merge_overlay",
        required=False,
        type=str,
        help="Path to a pdf of a page to be overlaid with the pages specified\
              with the -p argument (all if not specified)"
    )

    args = parser.parse_args()

    if args.wishto == "compress":
        assert args.gs_path is not None,\
               "You should specify GhostScript path to compress pdf file"
        compress_pdf(args.input_pdf, args.output_pdf,
                     args.power_compression, args.gs_path)
    elif args.wishto == "remove":
        pages = [int(p) for p in args.pages.split(',')]
        remove_pages(args.input_pdf, args.output_pdf, pages)
    elif args.wishto == "keep":
        pages = [int(p) for p in args.pages.split(',')]
        keep_pages(args.input_pdf, args.output_pdf, pages)
    elif args.wishto == "changeorder":
        pages = [int(p) for p in args.pages.split(',')]
        change_order(args.input_pdf, args.output_pdf, pages)
    elif args.wishto == "overlay":
        overlay_pdf_files(args.input_pdf, args.output_pdf,
                          args.merge_overlay, args.pages)
    elif args.wishto == "merge":
        merge_pdf_files(args.input_pdf, args.output_pdf)


if __name__ == '__main__':
    main()
