#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frame manager

Load all images from a directory or a video
Create a gif from the input

Args:
    - Path to the images or a video
    (OPTIONAL)
    - Output path
    - Extension if only images with specific extension is wanted
    - Add an image specified time to the end of the gif
    - FPS (default is 30)
    - Resize factor for the images to build the gif
    - Keep resized images into a separated folder
    - Frames to keep: if we want to keep 1 frame every N frames from the video
    - Number of gifs wanted to avoid having a huge one (default is 1)
    - Suffix to gif name

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
from PIL import Image, GifImagePlugin

import sys
from tqdm import tqdm


def extract_gif(gif_path, output_path, skip):
    gif_object = Image.open(gif_path)
    for i, frame in tqdm(enumerate(range(gif_object.n_frames))):
        gif_object.seek(frame)
        if i%skip == 0:
            gif_object.save(output_path + "frame_{0:08d}.png".format(i))


def extract_video(video_path, output_path, skip):
    vidoe_capture = cv2.VideoCapture(video_path)
    success, image = vidoe_capture.read()
    i = 0
    while success:
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        if i%skip == 0:
            cv2.imwrite(output_path + "frame_{0:08d}.png".format(i), image)    
        success, image = vidoe_capture.read()
        i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        type=str,
        help="Path to the images or a video."
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=False,
        default="",
        type=str,
        help="Path to the output gif."
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
        "-a",
        "--add_image",
        required=False,
        default=None,
        type=str,
        help="Path/to/img.png,number_of_times"
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
        type=float,
        help="Divide size of images n times (default is 1)."
    )
    parser.add_argument(
        "-k",
        "--keep_extracted_imgs",
        required=False,
        action="store_true",
        help="To keep the resized images (if -r option was specified)."
    )
    parser.add_argument(
        "-p",
        "--skip",
        required=False,
        default=1,
        type=int,
        help="To speed up the video, the script will keep 1 frame / skip."
    )
    parser.add_argument(
        "-n",
        "--gif_name",
        required=False,
        default="",
        type=str,
        help="Add suffix to the gif name."
    )

    args = parser.parse_args()
    input_directory = os.path.dirname(args.input_path) + '/'

    images_directory = input_directory

    if os.path.isfile(args.input_path):
        print("Extract images...")
        images_directory += 'tmp_images/'
        os.makedirs(images_directory, exist_ok=True)

        file_directory = os.path.dirname(args.input_path) + '/'
        if os.path.basename(args.input_path).split('.')[-1] == 'gif':
            extract_gif(args.input_path, images_directory, args.skip)
        if os.path.basename(args.input_path).split('.')[-1] == 'mp4':
            extract_video(args.input_path, images_directory, args.skip)

    images_list_path = sorted(glob(images_directory + '/*'))
    cv2_images = []

    print("\nRead images...")
    for i, image_path in tqdm(enumerate(images_list_path)):
        img = cv2.imread(image_path)
        if args.resize_fact is not None:
            img = cv2.resize(img, (int(img.shape[1]*args.resize_fact),
                                   int(img.shape[0]*args.resize_fact)))
        cv2_images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if args.add_image is not None:
        print("Add image...")
        img_path, times = \
            args.add_image.split(',')[0], args.add_image.split(',')[1]
        images = cv2.imread(img_path)
        images = cv2.resize(images, (img.shape[1], img.shape[0]))
        rgb_img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
        for _ in tqdm(range(int(times))):
            cv2_images.append(rgb_img)

    print("Create gif...")

    output_gif_path = ''
    output_gif_name = args.gif_name

    if args.gif_name == "":
        output_gif_name = "results.gif"
    elif args.gif_name.split('.')[-1] != 'gif':
        output_gif_name += '.gif'

    output_gif_path = args.output_path + '/' + output_gif_name
    if args.output_path == "":
        output_gif_path = input_directory + '/' + output_gif_name
    elif args.output_path.split('.')[-1] == 'gif':
        output_gif_path = args.output_path

    os.makedirs(os.path.dirname(output_gif_path), exist_ok=True)
    with imageio.get_writer(output_gif_path, mode="I", fps=args.fps) as writer:
        for i, frame in tqdm(enumerate(cv2_images)):
            writer.append_data(frame)
    writer.close()
    
    if not args.keep_extracted_imgs:
        [os.remove(img) for img in glob(images_directory + '/*')]
        os.rmdir(images_directory)


if __name__ == '__main__':
    main()
