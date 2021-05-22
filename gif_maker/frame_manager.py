#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frame manager

Extract frames from .gif/.mp4 input file (or load frames if directory as input)
Create a gif from the frames with options

Args:
    - Path to the images or a video
    (OPTIONAL)
    - Output path
    - Extension if only images with specific extension is wanted
    - Add an image to the end of the gif (n times)
    - FPS (default is 30)
    - Resize factor for the images to build the gif
    - Keep extracted images from the .gif/.mp4
    - Frames to keep: if we want to keep 1 frame every N frames from the video
    - gif name (default is result.gif)

Example:

    python gif_maker.py -i img_path/
    will create a gif at 30 fps as result.gif in the img_path directory

    - extract images from .mp4 video
    python gif_maker.py -i video.mp4 -p 4
    will extract all the video frames to tmp_images/ folder and create a gif
    at 30 fps with 1/4 of frames

    - extract images from .gif file
    python gif_maker.py -i mygif.gif -r 0.5 -n resized_gif.gif -k -f 10
    will extract all the gif frames from mygif.gif to tmp_images/ folder
    will create a new gif resized_gif.gif with resolution divided by 2, at 10 fps
    will not remove the tmp_images/ folder
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


def extract_gif(gif_path, output_path, skip, extension='png'):
    gif_object = Image.open(gif_path)
    for i, frame in tqdm(enumerate(range(gif_object.n_frames))):
        gif_object.seek(frame)
        if i%skip == 0:
            gif_object.save(
                output_path + "frame_{0:08d}.{1}".format(i, extension))


def extract_video(video_path, output_path, skip, extension='png'):
    vidoe_capture = cv2.VideoCapture(video_path)
    success, image = vidoe_capture.read()
    i = 0
    while success:
        sys.stdout.write("\rframe {0}".format(i))
        sys.stdout.flush()
        if i%skip == 0:
            cv2.imwrite(
                output_path + "frame_{0:08d}.{1}".format(i, extension), image)
        success, image = vidoe_capture.read()
        i += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        type=str,
        help="Path to a folder of images (with '\\') or a .gif/.mp4 file."
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
        default=1,
        type=float,
        help="Multiply image resolution by given number (default is 1)."
    )
    parser.add_argument(
        "-k",
        "--keep_extracted_imgs",
        required=False,
        action="store_true",
        help="To keep the resized images if input is a .gif/.mp4 file."
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
        default="result.gif",
        type=str,
        help="Output gif name."
    )

    args = parser.parse_args()
    input_directory = os.path.dirname(args.input_path) + '/'

    images_directory = input_directory

    # if input if gif or mp4: extract all images
    if os.path.isfile(args.input_path):
        print("Extract images...")
        images_directory += 'tmp_images/'
        os.makedirs(images_directory, exist_ok=True)

        file_directory = os.path.dirname(args.input_path) + '/'
        if os.path.basename(args.input_path).split('.')[-1] == 'gif':
            extract_gif(args.input_path, images_directory, args.skip)
        if os.path.basename(args.input_path).split('.')[-1] == 'mp4':
            extract_video(args.input_path, images_directory, args.skip)

    images_list_path = sorted(glob(images_directory + '/*' + args.extension))
    cv2_images = []

    print("\nRead images...")
    for i, image_path in tqdm(enumerate(images_list_path)):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (int(img.shape[1]*args.resize_fact),
                               int(img.shape[0]*args.resize_fact)))
        cv2_images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # add image at the end of the cv2_images list
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

    # get gif name
    output_gif_name = args.gif_name
    if args.gif_name.split('.')[-1] != 'gif':
        output_gif_name += '.gif'

    # get gif path
    output_gif_path = args.output_path + '/' + output_gif_name
    if args.output_path == "" and os.path.isfile(args.input_path):
        output_gif_path = input_directory + '/' + output_gif_name
    elif args.output_path == "":
        output_gif_path = input_directory + '/../' + output_gif_name
    elif args.output_path.split('.')[-1] == 'gif':
        output_gif_path = args.output_path

    # create gif
    os.makedirs(os.path.dirname(output_gif_path), exist_ok=True)
    with imageio.get_writer(output_gif_path, mode="I", fps=args.fps) as writer:
        for i, frame in tqdm(enumerate(cv2_images)):
            writer.append_data(frame)
    writer.close()
    
    if not args.keep_extracted_imgs and os.path.isfile(args.input_path):
        [os.remove(img) for img in glob(images_directory + '/*')]
        os.rmdir(images_directory)


if __name__ == '__main__':
    main()
