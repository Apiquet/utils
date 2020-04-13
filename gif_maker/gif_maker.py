#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gif maker

Load all images from a directory
Create a gif with them

Args:
    - Path to the images
    (OPTIONAL)
    - Output path
    - extension if only images with specific extension is wanted
    - FPS (default is 30)
    - resize factor for the images to build the gif
    - number of gifs wanted to avoid having a huge one (default is 1)

Example:

    - simple use:
    python gif_maker.py -i img_path/
    will create a gif at 30 fps as gif_0.gif in the img_path directory
    (optional)
    1- Change fps with -f option, -f 20 will set fsp to 20
    2- Add a suffix to the gif created with -s option
    3- Only select images with specific extension: -e option
        with -e png, the program will only select png images

    - resize images before creating the gif:
    python gif_maker.py -i img_path/ -r 2
    will create a img_path/tmp_imgs/ with all the images with size divided by 2
    will create a gif at 30 fps as gif_0.gif in the img_path directory
    (optional)
    To keep the tmp_folder/, specify -k option,
    otherwise it will be deleted

    - create multiple gif files:
    python gif_maker.py -i img_path/ -n 2
    will create two gif, each with half of the images
    This option divides the images into n parts for each gif.

    - advanced use:
    All the options can be combined, for instance:
    With a directory of images:
    ├──imgs/
    |  ├──0001.png
    |  ├──0002.jpg
    |  ├──0003.png
    |  ├──0004.png
    |  ├──0005.png

    python gif_maker.py -i img_path/ -f 15 -n 2 -s "test" -e png -r 2 -k
    will create:
    ├──imgs/
    |  ├──gif_0_test.gif
    |  ├──gif_1_test.gif
    |  ├──0001.png
    |  ├──...
    |  ├──tmp_imgs/
    |  |  ├──0001.png
    |  |  ├──0003.png
    |  |  ├──0004.png
    |  |  ├──0005.png

    gif_0_test.gif is a gif at 15 fps with 0001.png and 0003.png
    gif_1_test.gif is a gif at 15 fps with 0004.png and 0005.png
    The images' size were divided by 2 and stored under tmp_imgs/
"""

import argparse
import cv2
from glob import glob
import imageio
import numpy as np
import os
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--path_to_imgs",
        required=True,
        type=str,
        help="Path to the images."
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=False,
        default=None,
        type=str,
        help="Path to store playback images."
    )
    parser.add_argument(
        "-e",
        "--extension",
        required=False,
        default=".*",
        type=str,
        help="Extension to look for within the image dir."
    )
    parser.add_argument(
        "-f",
        "--fps",
        required=False,
        default=30,
        type=str,
        help="fps of the output gif, default is 30."
    )
    parser.add_argument(
        "-r",
        "--resize_fact",
        required=False,
        default=None,
        type=int,
        help="Divide size of images n times (default is 1)."
    )
    parser.add_argument(
        "-k",
        "--keep_resized_imgs",
        required=False,
        action="store_true",
        help="To keep the resized images (if -r option was specified)."
    )
    parser.add_argument(
        "-n",
        "--nb_gif",
        required=False,
        default=1,
        type=int,
        help="Set number of gif wanted (default is 1)."
    )
    parser.add_argument(
        "-s",
        "--suffix",
        required=False,
        default="",
        type=str,
        help="Add suffix to the gif name."
    )

    args = parser.parse_args()

    imgs = [img for img in sorted(glob(args.path_to_imgs + '/*' +
                                       args.extension))
            if ".gif" not in img]
    assert len(imgs) > 0, "No image found: " + args.path_to_imgs +\
        '/*' + args.extension

    if args.output_path is None:
        output_dir = args.path_to_imgs
    else:
        output_dir = args.output_path + '/'
        os.makedirs(output_dir, exist_ok=True)

    if args.resize_fact is not None:
        tmp_folder = args.path_to_imgs + '/tmp_imgs'
        os.makedirs(tmp_folder, exist_ok=True)
        for img_path in imgs:
            img = cv2.imread(img_path)
            img = cv2.resize(img, (img.shape[1] // args.resize_fact,
                                   img.shape[0] // args.resize_fact))
            cv2.imwrite(tmp_folder + '/' + os.path.basename(img_path), img)
        imgs = [img for img in sorted(glob(tmp_folder + '/*' + args.extension))
                if ".gif" not in img]

    for i, el in enumerate(np.array_split(imgs, args.nb_gif)):
        with imageio.get_writer(output_dir + "gif_" + str(i) + '_' +
                                args.suffix + '.gif', mode='I',
                                fps=args.fps) as writer:
            for img_path in tqdm(el):
                image = imageio.imread(img_path)
                writer.append_data(image)

    if args.keep_resized_imgs is False and args.resize_fact is not None:
        [os.remove(img) for img in glob(tmp_folder + '/*')]
        os.rmdir(tmp_folder)


if __name__ == '__main__':
    main()
