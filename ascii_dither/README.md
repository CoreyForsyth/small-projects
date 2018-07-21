Usage: python image_process.py [options] <file>

Applys Floyd-Steinberg dither algorithm to input image, saves as image/ascii

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

example usage:
python image_process.py -ia -w 100 -s 8 -m dither cat.jpg

What actually happens during the example usage:

1. The input image is resized to the input width (100), keeping aspect ratio (width option)
2. This is converted to a greyscale image
3. The palette is reduced 8, using the dither method (shade, method option)
4. This is then converted to ascii and saved as dither_100w_8s.txt (ascii option)
5. The image is also saved as an image to dither_100w_8s.png (image option)