#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gif maker

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
from PIL import Image, ImageSequence
import sys
from tqdm import tqdm


def analyseImage(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable.
    Need to know the mode before processing all frames.
    """
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def extract_and_resize_frames(path, resize_to=None):
    """
    Iterate the GIF, extracting each frame and resizing them

    Returns:
        An array of all frames
    """
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    if not resize_to:
        resize_to = (im.size[0] // 2, im.size[1] // 2)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []

    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))

            new_frame.thumbnail(resize_to, Image.ANTIALIAS)
            all_frames.append(new_frame)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames


def resize_gif(path, save_as=None, resize_to=None):
    """
    Resizes the GIF to a given length:

    Args:
        path: the path to the GIF file
        save_as (optional): Path of the resized gif.
        If not set, the original gif will be overwritten.
        resize_to (optional): new size of the gif. Format: (int, int).
        If not set, the original GIF will be resized to half of its size.
    """
    all_frames = extract_and_resize_frames(path, resize_to)

    if not save_as:
        save_as = path

    if len(all_frames) == 1:
        print("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True,
                           append_images=all_frames[1:], loop=1000)


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
        "-a",
        "--add_image",
        required=False,
        default=".*",
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
        "-p",
        "--skip",
        required=False,
        default=1,
        type=int,
        help="To speed up the video, the script will keep 1 frame / skip."
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

    if args.output_path is None:
        output_dir = os.path.dirname(args.input_path) + '/'
    else:
        output_dir = args.output_path + '/'
        os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(args.input_path):
        reader = imageio.get_reader(args.input_path)
        if args.fps is None:
            fps = reader.get_meta_data()['fps']
        else:
            fps = args.fps

        output_gif = output_dir + 'video2gif' + args.suffix + '.gif'
        writer = imageio.get_writer(output_gif, fps=fps)
        for i, img in enumerate(reader):
            if i % args.skip == 0:
                sys.stdout.write("\rframe {0}".format(i))
                sys.stdout.flush()
                writer.append_data(img)
        if args.add_image is not None:
            path_n_times = args.add_image.split(',')
            img_path, times = path_n_times[0], path_n_times[1]
            image = cv2.imread(img_path)
            image = cv2.resize(image, (img.shape[1], img.shape[0]))
            cv2.imwrite(os.path.dirname(img_path) + '/res_' +
                        os.path.basename(img_path), image)
            image = imageio.imread(os.path.dirname(img_path) +
                                   '/res_' + os.path.basename(img_path))
            for i in tqdm(range(int(times))):
                writer.append_data(image)
        writer.close()

        if args.resize_fact is not None:
            img = Image.open(output_gif)
            new_size = (img.size[0]//args.resize_fact,
                        img.size[1]//args.resize_fact)
            resize_gif(output_gif, save_as=None, resize_to=new_size)
        return

    imgs = [img for img in sorted(glob(args.input_path + '/*' +
                                       args.extension))
            if ".gif" not in img]
    assert len(imgs) > 0, "No image found: " + args.input_path +\
        '/*' + args.extension

    if args.resize_fact is not None:
        tmp_folder = args.input_path + '/tmp_imgs'
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
