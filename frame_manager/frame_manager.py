#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Frame manager

Extract frames from .gif/videos input file (or load frames if directory as input)
Create a gif from the frames with options

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

from argparse import ArgumentParser
from glob import glob
from math import cos, radians, sin
from os import makedirs, path, remove, rmdir
from sys import stdout, float_info

import cv2
from imageio import get_writer
from numpy import array, ndarray
from PIL import Image
from tqdm import tqdm


def overlap_two_images(img1: Image, img2: Image) -> array:
    """
    Function to overlap segmentation map with image

    Args:
        - img1: first image
        - img2: second image
    Return:
        - overlap between the two input images
    """
    img1.paste(img2, (0, 0), img2.convert('RGBA'))

    return array(img1)


def extract_gif(result_path: str, output_path: str, skip: int, start_idx: int, end_idx: int) -> int:
    """Extract images from a .gif file to the output_path folder (.png images)

    Args:
        - result_path: input gif to extract
        - output_path: path for output .png images
        - skip: reduce the number of images: keep 1 frame/skip
        - start_idx: start index to save images
        - end_idx: end index to save images
    Return:
        - number of frames extracted
    """
    gif_object = Image.open(result_path)
    for i, frame in tqdm(enumerate(range(gif_object.n_frames))):
        if i < start_idx:
            continue
        elif i > end_idx:
            break
        gif_object.seek(frame)
        if i % skip == 0:
            gif_object.save(output_path + "frame_{0:08d}.png".format(i))
    return gif_object.n_frames


def extract_video(
    video_path: str, output_path: str, skip: int, start_idx: int, end_idx: int
) -> int:
    """Extract images from a .mp4 file to the output_path folder (.png images)

    Args:
        - result_path: input video to extract
        - output_path: path for output .png images
        - skip: reduce the number of images: keep 1 frame/skip.
        - start_idx: start index to save images
        - end_idx: end index to save images
    Return:
        - number of frames extracted
    """
    video_capture = cv2.VideoCapture(video_path)
    success, image = video_capture.read()
    i = -1
    while success:
        i += 1
        if i < start_idx:
            continue
        elif i > end_idx:
            break
        stdout.write("\rframe {0}".format(i))
        stdout.flush()
        if i % skip == 0:
            cv2.imwrite(output_path + "frame_{0:08d}.png".format(i), image)
        success, image = video_capture.read()
    return i


def rotate_image(image: ndarray, angle_deg: float) -> ndarray:
    """Extract images from a .mp4 file to the output_path folder (.png images)

    Args:
        - image: input image to rotate
        - angle_deg: angle in degrees
    Return:
        - rotated image
    """
    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)

    rot = cv2.getRotationMatrix2D(img_c, angle_deg, 1)

    rad = radians(angle_deg)
    sinus = sin(rad)
    cosinus = cos(rad)
    b_w = int((h * abs(sinus)) + (w * abs(cosinus)))
    b_h = int((h * abs(cosinus)) + (w * abs(sinus)))

    rot[0, 2] += (b_w / 2) - img_c[0]
    rot[1, 2] += (b_h / 2) - img_c[1]

    outImg = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)
    return outImg


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_path",
        required=True,
        type=str,
        help="Path to a folder of images (with '\\') or a .gif/.mp4 file.",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=False,
        default=None,
        type=str,
        help="Path to the output file.",
    )
    parser.add_argument(
        "-e",
        "--extension",
        required=False,
        default=".*",
        type=str,
        help="Extension to look for within the image dir.",
    )
    parser.add_argument(
        "-a",
        "--add_image",
        required=False,
        default=None,
        type=str,
        help="Path/to/img.png,number_of_times",
    )
    parser.add_argument(
        "-f",
        "--fps",
        required=False,
        default=30,
        type=int,
        help="fps of the output result, default is 30.",
    )
    parser.add_argument(
        "-r",
        "--resize_fact",
        required=False,
        default=1.0,
        type=float,
        help="Multiply image resolution by given number (default is 1).",
    )
    parser.add_argument(
        "-t",
        "--rotate_angle",
        required=False,
        default=0.0,
        type=float,
        help="Angle in degrees to rotate image (default is 0).",
    )
    parser.add_argument(
        "-k",
        "--keep_extracted_imgs",
        required=False,
        action="store_true",
        help="To keep the resized images if input is a .gif/.mp4 file.",
    )
    parser.add_argument(
        "-p",
        "--skip",
        required=False,
        default=1,
        type=int,
        help="To reduce the gif size, the script will keep 1 frame / skip.",
    )
    parser.add_argument(
        "-n", "--result_name", required=False, default="result", type=str, help="Output name."
    )
    parser.add_argument(
        "-v",
        "--overlap",
        required=False,
        default=None,
        type=str,
        help="Image to overlap with all the others.",
    )
    parser.add_argument(
        "-m",
        "--mp4",
        required=False,
        action="store_true",
        help="To create mp4 video instead of gif file.",
    )
    parser.add_argument(
        "-g",
        "--padding",
        required=False,
        default=None,
        type=str,
        help="Padding to add in format: top,bottom,left,right,boderType,r,g,b",
    )
    parser.add_argument(
        "-s",
        "--start_idx",
        required=False,
        default=0,
        type=int,
        help="Start frame index.",
    )
    parser.add_argument(
        "-d",
        "--end_idx",
        required=False,
        default=float_info.max,
        type=int,
        help="End frame index.",
    )

    args = parser.parse_args()
    input_directory = path.abspath(path.dirname(args.input_path)) + '/'

    images_directory = input_directory

    index_used_for_extraction = False

    # if input if gif or video: extract all images
    if path.isfile(args.input_path):
        index_used_for_extraction = True
        images_directory += 'tmp_images/'
        makedirs(images_directory, exist_ok=True)

        if path.basename(args.input_path).split('.')[-1] in ['gif', 'GIF']:
            print("Extract gif image...")
            number_of_frames = extract_gif(
                args.input_path, images_directory, args.skip, args.start_idx, args.end_idx
            )
        else:
            print("Extract video file...")
            number_of_frames = extract_video(
                args.input_path, images_directory, args.skip, args.start_idx, args.end_idx
            )

        if number_of_frames == 0:
            raise Exception("Extraction error.")
    elif not path.isdir(args.input_path):
        raise Exception(args.input_path + " does not exist.")

    images_list_path = sorted(glob(images_directory + '/*' + args.extension))
    if not index_used_for_extraction:
        images_list_path = images_list_path[args.start_idx : args.end_idx]
    if len(images_list_path) == 0:
        raise Exception('Not file found with pattern: ' + images_directory + '/*' + args.extension)

    cv2_images = []

    print("\nRead images...")
    if args.overlap is not None:
        overlap_image = Image.open(args.overlap)

    if args.padding is not None:
        top, bottom, left, right, boderType, r, g, b = [int(el) for el in args.padding.split(',')]

    for i, image_path in tqdm(enumerate(images_list_path)):
        img = cv2.imread(image_path)
        img = cv2.resize(
            img, (int(img.shape[1] * args.resize_fact), int(img.shape[0] * args.resize_fact))
        )
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if args.overlap is not None and i < 38:
            rgb_img = overlap_two_images(Image.fromarray(rgb_img), overlap_image)
        if args.rotate_angle != 0.0:
            rgb_img = rotate_image(rgb_img, args.rotate_angle)
        if args.padding is not None:
            rgb_img = cv2.copyMakeBorder(
                rgb_img, top, bottom, left, right, boderType, value=[r, g, b]
            )
        cv2_images.append(rgb_img)

    img_height, img_width, _ = rgb_img.shape

    # add image at the end of the cv2_images list
    if args.add_image is not None:
        print("Add image...")
        img_path, times = args.add_image.split(',')[0], args.add_image.split(',')[1]
        images = cv2.imread(img_path)
        images = cv2.resize(images, (img_width, img_height))
        rgb_img = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
        for _ in tqdm(range(int(times))):
            cv2_images.append(rgb_img)

    print("Create animation...")

    # get result path
    output_result_path = args.output_path + '/' + args.result_name
    if args.output_path is None:
        output_result_path = input_directory + '/' + args.result_name

    if args.mp4:
        if args.result_name.split('.')[-1] != 'mp4':
            output_result_path += '.mp4'
        video = cv2.VideoWriter(
            output_result_path, cv2.VideoWriter_fourcc(*'mp4v'), args.fps, (img_width, img_height)
        )

        for image in tqdm(cv2_images):
            video.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        video.release()
    else:
        if args.result_name.split('.')[-1] not in ['gif', 'GIF']:
            output_result_path += '.gif'
        # create gif
        makedirs(path.dirname(output_result_path), exist_ok=True)
        with get_writer(output_result_path, mode="I", fps=args.fps) as writer:
            for frame in tqdm(cv2_images):
                writer.append_data(frame)
        writer.close()

    if not args.keep_extracted_imgs and path.isfile(args.input_path):
        [remove(img) for img in glob(images_directory + '/*')]
        rmdir(images_directory)


if __name__ == '__main__':
    main()
