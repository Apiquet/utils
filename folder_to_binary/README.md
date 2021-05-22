# Folder to binary:
    - Convert a folder of files to a simple .bin file
    - extract the .bin file to get the folder

# Args:
    - Path to the folder
    - name for the .bin file (default is folder_name.bin)

# Examples:

## binarize folder:
    python folder_to_binary.py -i myfolder/
    will create myfolder.bin with all files

## extract .bin file:
    python folder_to_binary.py -i mybin.bin
    will create mybin.bin to mybin/ with all files
