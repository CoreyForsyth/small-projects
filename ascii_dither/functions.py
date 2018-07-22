from __future__ import print_function
from PIL import Image, ImageFile
import numpy as np

def usage():
    print

def new_color(inColor, error):
    outColor = inColor + error
    if outColor < 0:
        outColor = 0
    elif outColor > 255:
        outColor = 255
    return outColor

def dither(image, palette_width):
    x = image.shape[0]
    y = image.shape[1]
    for i in range(0, x):
        for j in range(0, y):
            oldpixel = image[i][j]
            newpixel = ((oldpixel +palette_width/2)  / palette_width) * palette_width
            image[i][j] = newpixel
            quant_error = oldpixel - newpixel
            if i != x -1:
                image[i + 1][j    ] = new_color(image[i + 1][j    ], quant_error * 7 / 16)
            if i != 0 and j != y - 1:
                image[i - 1][j + 1] = new_color(image[i - 1][j + 1], quant_error * 3 / 16)
            if j != y - 1:
                image[i    ][j + 1] = new_color(image[i    ][j + 1], quant_error * 5 / 16)
            if j != y - 1 and i != x - 1:
                image[i + 1][j + 1] = new_color(image[i + 1][j + 1], quant_error * 1 / 16)
    return image


def reduce_palette(image, palette_width):
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            image[i][j] = ((image[i][j] +palette_width/2)  / palette_width) * palette_width
    return image

def resize(image, ratio):
    new_width = int(float(image.size[0]) * float(ratio))
    new_height = int(float(image.size[1]) * float(ratio))
    return image.resize((new_width,new_height), Image.ANTIALIAS)

def remove_color(color_image):
    size = [color_image.shape[0], color_image.shape[1]]
    bw_image = np.empty(size, dtype=np.uint8)
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            bw_image[x][y] = color_image[x][y][0]/3 + color_image[x][y][1]/3 + color_image[x][y][2]/3
    return bw_image

def save_black_and_white_image(image, output_name):
    outIm = Image.fromarray(image, 'L')
    outIm.save(output_name + ".png", 'PNG', quality=100)

def save_as_ascii(image, palette_width, shades, character_set, output_name, negative):
    file = open(output_name + ".txt", "w+")
    multiplier = int(len(character_set) / shades)
    charset_length = len(character_set) - 1
    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            index = (image[i][j] + palette_width/2)  / palette_width
            index = int(multiplier * index)
            if negative:
                file.write(character_set[charset_length - index])
                print(index)
            else:
                file.write(character_set[index])

        file.write('\n')
    file.close()
    return