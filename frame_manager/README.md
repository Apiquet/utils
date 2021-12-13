# Frame manager:
    - Extract frames from .gif/.mp4 input file
    - load frames if directory as input
    - Create a gif from the input
    - Options available: set fps, set specific image extension, resize images, customize gif name, skip frames to reduce gif size, keep or not the extracted images from the input file, add padding, rotate images.

# Args:
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
    - path to an image to overlap with all the input images
    - option to save an mp4 video instead of gif file
    - size of padding on top,bottom,left,right,boderType,r,g,b
    - rotate images


# Examples:

## folder as input:
    python gif_maker.py -i img_path/
    will create a gif at 30 fps as result.gif in the img_path directory

## video as input and reduce number of frame for the gif:
    - extract images from .mp4 video
    python gif_maker.py -i video.mp4 -p 4
    will extract all the video frames to tmp_images/ folder and create a gif
    at 30 fps with 1/4 of frames

## gif as input, change resolution, set fps and keep extracted images:
    - extract images from .gif file
    python gif_maker.py -i mygif.gif -r 0.5 -n resized_gif.gif -k -f 10
    will extract all the gif frames from mygif.gif to tmp_images/ folder
    will create a new gif resized_gif.gif with resolution divided by 2, at 10 fps
    will not remove the tmp_images/ folder
