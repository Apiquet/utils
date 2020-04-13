# Gif maker:
    - Load all images from a directory
    - Create a gif with them
    - Options available: set fps, set specific image extension, divide the images into several gif files, resize images, customize gif name.

# Args:
    - Path to the images
    (OPTIONAL)
    - Output path
    - Extension if only images with specific extension is wanted
    - FPS (default is 30)
    - Resize factor for the images to build the gif
    - Keep resized images into a separated folder
    - Number of gifs wanted to avoid having a huge one (default is 1)
    - Suffix to gif name


# Examples:
## simple use:
    python gif_maker.py -i img_path/
    will create a gif at 30 fps as gif_0.gif in the img_path directory
    (optional)
    1- Change fps with -f option, -f 20 will set fsp to 20
    2- Add a suffix to the gif created with -s option
    3- Only select images with specific extension: -e option
        with -e png, the program will only select png images

## resize images before creating the gif:
    python gif_maker.py -i img_path/ -r 2
    will create a img_path/tmp_imgs/ with all the images with size divided by 2
    will create a gif at 30 fps as gif_0.gif in the img_path directory
    (optional)
    To keep the tmp_folder/, specify -k option,
    otherwise it will be deleted

## create multiple gif files:
    python gif_maker.py -i img_path/ -n 2
    will create two gif, each with half of the images
    This option divides the images into n parts for each gif.

## advanced use:
    All the options can be combined, for instance:
    With a directory of images:
    |--imgs/
    |--|--0001.png
    |--|--0002.jpg
    |--|--0003.png
    |--|--0004.png
    |--|--0005.png

    python gif_maker.py -i img_path/ -f 15 -n 2 -s "test" -e png -r 2 -k
    will create:
    |--imgs/
    |--|--gif_0_test.gif
    |--|--gif_1_test.gif
    |--|--0001.png
    |--|--...
    |--|--tmp_imgs/
    |--|--|--0001.png
    |--|--|--0003.png
    |--|--|--0004.png
    |--|--|--0005.png

    gif_0_test.gif is a gif at 15 fps with 0001.png and 0003.png
    gif_1_test.gif is a gif at 15 fps with 0004.png and 0005.png
    The images' size were divided by 2 and stored under tmp_imgs/
