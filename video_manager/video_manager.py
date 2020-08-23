#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Video manager

Args:
    - Path to the video(s)
    - Path to the output video

Example:
    python3 video_manager.py -i path/to/video.mp4 -o path/to/output_video.mp4
"""

import argparse
import cv2
from glob import glob


def extract(compressedfile, extract_path):
    '''Extract files

    Args:
        - compressedfile    (str) : path to the compressed file
        - extract_path      (str) : path for the extracted files
    '''
    shutil.unpack_archive(compressedfile, extract_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        type=str,
        help="Folder containing video(s)."
    )
    parser.add_argument(
        "-w",
        "--wish",
        choices=['speedup', 'concat'],
        required=True,
        type=str,
        help="Action wanted."
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
        "-f",
        "--fps",
        required=False,
        type=int,
        default=30,
        help="New fps to set"
    )
    parser.add_argument(
        "-o",
        "--output_name",
        required=True,
        type=str,
        help="Output path."
    )

    args = parser.parse_args()
    
    videos_path = sorted(glob(args.input + "/*"))
    
    out = cv2.VideoWriter(args.input + '/' + args.output_name + '.avi',
                          cv2.VideoWriter_fourcc('M','J','P','G'),
                          args.fps, (1920,1080))
    
    for video_path in videos_path:
        cap = cv2.VideoCapture(video_path)

        i = 0
        while(cap.isOpened()):
            i = i + 1
            ret, frame = cap.read()
            if ret and i%args.skip == 0:
                out.write(frame)
            elif not ret:
                break

        cap.release()
    out.release()


if __name__ == '__main__':
    main()
