#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Concatenate list of videos or folder of videos, change speed and resize videos

Args:
    - Path to the video(s)
    (OPTIONAL)
    - Output path
    - FPS (default is 30)
    - Resize factor for the images to build the gif
    - Frames to keep: if we want to keep 1 frame every N frames from the video

Example to concatenate multiple videos within a folder and change the fps:
    python3 video_manager.py -i path/to/folder_with_videos/ --fps 60

Example to concatenate two videos and reduce the output resolution by 3:
    python3 video_manager.py -i path/to/video1.mp4,path/to/video2.mp4 -r 3
"""

import argparse
import cv2
from glob import glob
import os
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_videos",
        required=True,
        type=str,
        help="Video path separated by a comma."
    )
    parser.add_argument(
        "-k",
        "--skip",
        required=False,
        type=int,
        default=1,
        help="Interval of frame to skip to avoid having a huge\
        video with a crazy FPS."
    )
    parser.add_argument(
        "--fps",
        required=False,
        type=int,
        default=30,
        help="New fps to set"
    )
    parser.add_argument(
        "-r",
        "--resize_fact",
        required=False,
        default=1,
        type=float,
        help="Divide size of images n times (default is 1)."
    )
    parser.add_argument(
        "-o",
        "--output_path",
        required=False,
        type=str,
        help="Output path."
    )

    args = parser.parse_args()

    if os.path.isdir(args.input_videos):
        videos_path = sorted(glob(args.input_videos + "/*"))
    else:
        videos_path = args.input_videos.split(',')

    if args.output_path is None:
        args.output_path = os.path.dirname(videos_path[0]) +\
            '/output_video.mp4'

    vcap = cv2.VideoCapture(videos_path[0])
    width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH) // args.resize_fact)
    height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT) // args.resize_fact)

    out = cv2.VideoWriter(args.output_path, 0x7634706d,
                          args.fps, (width, height))

    for video_path in tqdm(videos_path):
        cap = cv2.VideoCapture(video_path)
        i = 0
        while(cap.isOpened()):
            i = i + 1
            ret, frame = cap.read()
            if ret and i % args.skip == 0:
                frame = cv2.resize(frame, (width, height))
                out.write(frame)
            elif not ret:
                break

        cap.release()
    out.release()


if __name__ == '__main__':
    main()
