# Video manager:
    - Change resolution of video(s)
    - Change fps of video(s)
    - Remove 1/N frames to reduce the videos' size
    - Concatenate videos from a list or a folder

# Args:
    - Path to the video(s)
    (OPTIONAL)
    - Output path
    - FPS (default is 30)
    - Resize factor for the images to build the gif
    - Frames to keep: if we want to keep 1 frame every N frames from the video

# Examples:
## Example to concatenate multiple videos within a folder and change the fps:
    python3 video_manager.py -i path/to/folder_with_videos/ --fps 60

## Example to concatenate two videos and reduce the output resolution by 3:
    python3 video_manager.py -i path/to/video1.mp4,path/to/video2.mp4 -r 3
