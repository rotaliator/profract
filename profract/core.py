from __future__ import print_function
import sys
from itertools import product, repeat
from functools import partial
from array import array
import time
import png

IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            return False
        self.interval = time.time() - self.start
        return self

def scale(comp_size, pixel_size, pixel):
    return pixel*comp_size / pixel_size

def mandel_for(re, im, max_dist=2**6, max_iter=255):
    z_re, z_im = re, im
    for i in range(max_iter):
        z_re, z_im = z_re*z_re - z_im*z_im + re, 2*z_re*z_im + im
        if ((z_re*z_re + z_im*z_im) >= max_dist):
            return i
    return max_iter

def mandel(re1, im1, re2, im2, width, height):
    """
    Calculates iterations of mandelbrot set into array of floats
    pure Python reference implementation
    re1, im1 - upper left corner
    re2, im2 - lower right corner
    width, height - size of output image
    """
    a = array('B', repeat(255, width*height))
    comp_size_re = re2 - re1
    comp_size_im = im2 - im1
    scale_re = partial(scale, comp_size_re, width)
    scale_im = partial(scale, comp_size_im, height)
    for y, x in product(range(height), range(width)):
        index = x + y*width
        a[index] = mandel_for(re1+scale_re(x), im1+scale_im(y))
    return a


def main():
    try:
        outfile = sys.argv[1]
    except IndexError:
        outfile = "mandel.png"

    with Timer() as t:
        m = mandel(-2.0, -1.0, 1.0, 1.0, IMAGE_WIDTH, IMAGE_HEIGHT)
    print("Calculations took: {:.2f} sec".format( t.interval))
    writer = png.Writer(width=IMAGE_WIDTH, height=IMAGE_HEIGHT, greyscale=True)
    with open(outfile, "wb") as f:
        writer.write_array(f, m)

if __name__ == '__main__':
    main()
