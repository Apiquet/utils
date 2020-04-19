# PDF manager:
    - remove pages
    - change pages order
    - compress pdf
     - overlay each pdf page with a one page pdf
      (useful to add a signature at specific pages
      or to put "confidential" on all pages)

# Args:
    - Path to the pdf file
    - Option wanted
    - List of pages concerned


# Examples:
## compression:
    install GhostScript from https://www.ghostscript.com/download/gsdnld.html
    then run:
    python pdf_manager.py -i input.pdf -o output.pdf\
        -w compress -g path/to/gswin64c.exe
    optional: -c can be add to set the power compression from 1 to 5

## keep some pages:
    To keep the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,3,4 -w keep

## remove some pages:
    To remove the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,3,4 -w remove

## change pages order:
    To change to pages order to page 3 then 2 then 1, run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,1,0 -w changeorder

## Overlay specified pages with a one page pdf:
    To overlay pages 2, 3 and 4 with the one page pdf 'overlay.pdf' run:
    python pdf_manager.py -i test.pdf -o output.pdf -w overlay
        -m overlay.pdf -p 1,2,3
    Do not specify -p if you want to overlay on all pages

## Merge several pdf files:
    To merge pdf files '1.pdf', '2.pdf', '3.pdf' run:
    python pdf_manager.py -i 1.pdf,2.pdf,3.pdf -o output.pdf -w merge
