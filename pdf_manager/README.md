# PDF manager:
    - remove pages
    - change pages order
    - compress pdf
    - add signature to pages (TODO)

# Args:
    - Path to the pdf file
    - Option wanted
    - List of pages concerned


# Example:
    *- compression:*
    install GhostScript from https://www.ghostscript.com/download/gsdnld.html
    then run:
    python pdf_manager.py -i input.pdf -o output.pdf\
        -w compress -g path/to/gswin64c.exe
    optional: -c can be add to set the power compression from 1 to 5

    *- keep some pages:*
    To keep the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,3,4 -w keep

    *- remove some pages:*
    To remove the pages 2, 3 and 4 run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,3,4 -w remove

    *- remove some pages:*
    To change to page order to page 3 then 2 then 1, run:
    python pdf_manager.py -i input.pdf -o output.pdf -p 2,1,0 -w changeorder