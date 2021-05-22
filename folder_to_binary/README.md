# Folder to binary:
    - Convert a folder of files to a simple .bin file
    - extract the .bin file to get the folder

# Args:
    - Path to the folder
    - name for the output file, default is:
        folder_name_bin if folder as input
        binary_name_extracted if file as input
    - delimiter to use

# Examples:

## binarize folder:
    python folder_to_binary.py -i myfolder/
    will create myfolder.bin with all files

## extract .bin file:
    python folder_to_binary.py -i mybin.bin
    will create mybin/ with all files
