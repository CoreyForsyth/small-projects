#!/usr/bin/env python2
from __future__ import print_function
from PIL import Image, ImageFile
import numpy as np
import getopt, sys
from functions import *

def usage():
    print("\nUsage: python " + sys.argv[0] + " [options] <file>\n")
    print("""Applys Floyd-Steinberg dither algorithm to input image, saves as image/ascii\n
Options:
-i, --image             saves output as bmp image
-a, --ascii             saves output as text file
-m, --method <arg>      method to use to decrease
                          greyscale palette
                          options: dither, simple
-w, --width <arg>       width of the text/image output
                          between 50 and 200
-s, --shades <arg>      amount of shades to use when 
                          decreasing palette
                          2-255
-o, --output <arg>      prepend arg to output file names
-h, --help              display this help and exit

example usage:""")
    print("python " + sys.argv[0] + " -ia -w 100 -s 8 -m dither cat.jpg\n")

# Global variables
if len(sys.argv) < 2:
    usage()
    exit(2)
input_location = sys.argv[1]
output_name = ""
acceptable_methods = ('dither', 'simple')
character_set = ('%', '#', '*', '=', '-', ':', '.', ' ')
width = 100
shades = 7
save_ascii = True
save_image = True
method = 'simple'

# Process arguments
if(len(sys.argv) < 2):
    usage()
    exit(2)
arg_list = sys.argv[1:]
unixOptions = "hm:iaw:s:o:"
gnuOptions = ["help", "method=", "image", "ascii", "width=", "shades=", "output="]
try:  
    arguments, values = getopt.getopt(arg_list, unixOptions, gnuOptions)
except getopt.error as err:
    print(str(err))
    usage()
    sys.exit(2)
for currentArgument, currentValue in arguments:  
    if currentArgument in ("-h", "--help"):
        usage()
        exit(0)
    if currentArgument in ("-m", "--method"):
        if currentValue in acceptable_methods:
            method = currentValue
    elif currentArgument in ("-w", "--width"):
        width = currentValue if int(currentValue) <= 200 and int(currentValue > 50) else 100
    elif currentArgument in ("-i", "--image"):
        save_image = True
    elif currentArgument in ("-a", "--ascii"):
        save_ascii = True
    elif currentArgument in ("-s", "--shades"):
        shades = int(currentValue) - 1
    elif currentArgument in ("-o", "--output"):
        output_name = currentValue

# Begin processing
input_location = sys.argv[len(sys.argv) - 1]
im = Image.open(input_location)
im = resize(im, float(width)/float(im.size[0]))
as_pixels = np.asarray(im, dtype=np.uint8)
bw_image = remove_color(as_pixels)
if method == 'dither':
    bw_image = dither(bw_image, 255 / shades)
elif method == 'simple':
    bw_image = reduce_palette(bw_image, 255 / shades)
output_file_name = method + '_' + str(width) + 'w_' + str(shades + 1) + 's'
if output_name != "":
    output_file_name = output_name + '_' + output_file_name
if save_ascii:
    save_as_ascii(bw_image, 255 / shades, shades + 1, character_set, output_file_name)
if save_image:
    save_black_and_white_image(bw_image, output_file_name)