[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/gopaljigaur/img2ascii) 

[![PyPI version](https://badge.fury.io/py/img2ascii.svg)](https://badge.fury.io/py/img2ascii) 
# Image2ASCII

img2ascii is a library written in python which can convert image or video files to ASCII

Option list:

- `-h` or `--help`       : To generate the help text
- `-m` or `--mode`       : Select the mode of operation -- `t` for text, `i` for image, `v` for video and `w` for webcam input
- `-c` or `--color`      : Optional parameter to select color mode. 0 - B/W, 1 - Grayscale and 2 - RGB. Default color mode is B/W
- `--fcolor`             : Optional parameter to set the text color in binary color mode. Default = white
- `--bcolor`             : Optional parameter to set the background color in binary color mode. Default = black<br>
<b>INFO:</b> For `--fcolor` and `--bcolor`, you can use color names - `white`, `black`, `red`, `green`, `blue`, `yellow`, `cyan` and `magenta`. To use other colors, hex codes for those colors must be supplied. Example - `ffcc99`.
- `-k` or `--kernel`     : Optional parameter to set the kernel size, default is 7px
- `-d` or `--density`    : Optional parameter to set the ASCII text density on image, default is 0.3 units; Range - (0,1) (exclusive)
- `-i` or `--ifile`      : Path to the input file for image and video modes
- `-o` or `--ofile`      : Path to the output file for image and video modes
- `-s` or `--cam_source` : Camera to be used for webcam mode. Use 0,1,2,3... to select cameras connected to the PC. Default value is 0
- `-f` or `--fancy`      : Fancy mode :). (Color mode defaults to RGB)

Installation:
- <b>Direct install : </b>
<t>- `python3 -m pip install img2ascii`
- <b>From Git : </b><br>
<t>1. `git clone https://github.com/gopaljigaur/img2ascii.git`<br>
<t>2. `cd img2ascii`<br>
<t>3. `python3 setup.py build`<br>
<t>4. `python3 setup.py install`

Usage :

- <b>For text</b> : `img2ascii.py -m t -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]`
- <b>For image :</b> `img2ascii.py -m i -c[color mode (optional)] --fcolor <text_color_hex>[optional] --bcolor <background_color_hex>[optional] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional] -f <fancy_mode>[optional]`
- <b>For video :</b> `img2ascii.py -m v -c[color mode (optional)] --fcolor <text_color_hex>[optional] --bcolor <background_color_hex>[optional] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional] -f <fancy_mode>[optional]`
- <b>For webcam :</b> `img2ascii.py -m w -c[color mode (optional)] --fcolor <text_color_hex>[optional] --bcolor <background_color_hex>[optional] -k <kernel_size>[optional] -d <text_density>[optional -s <source_camera (0,1,2...)>[optional] -f <fancy_mode>[optional]`

Usage in python code:

- <b>For text :</b> `from img2ascii import text_gen`<br> 
<t>then `text_gen.generate_ascii_t(str inputfile, str outputfile, int kernel [o], float density [o])`<br>
- <b>For image :</b> `from img2ascii import image_gen`<br> 
<t>then `image_gen.generate_ascii_i(str inputfile, str outputfile, int color [o], int kernel [o], float density [o], bool fancy [o], tuple(int) fcolor [o], tuple(int) bcolor [o])`<br>
- <b>For video :</b> `from img2ascii import video_gen`<br> 
<t>then `video_gen.generate_ascii_v(str inputfile, str outputfile, int color [o], int kernel [o], float density [o], bool fancy [o], tuple(int) fcolor [o], tuple(int) bcolor [o])`<br>
- <b>For webcam :</b> `from img2ascii import image_gen`<br> 
<t>then `image_gen.generate_ascii_w(int color [o], int kernel [o], float density [o], int cam_source [o], str cam_name [o], bool fancy [o], tuple(int) fcolor [o], tuple(int) bcolor [o])`

<b>NOTE :</b> Parameters followed by [o] are optional

Also, thanks to [Andrea Schiavinato](https://github.com/bunkahle) for [pygrabber](https://github.com/bunkahle/pygrabber)
