from multiprocessing import Pool
from .pure_python import scale, mandel_for

from array import array
from itertools import repeat, product
from functools import partial

def f(re_im):
    re, im = re_im
    return mandel_for(re, im)

def mandel(re1, im1, re2, im2, width, height):
    """
    Calculates iterations of mandelbrot set into array of floats
    Multiprocessing implementation
    re1, im1 - upper left corner
    re2, im2 - lower right corner
    width, height - size of output image
    """
    comp_size_re = re2 - re1
    comp_size_im = im2 - im1
    scale_re = partial(scale, comp_size_re, width)
    scale_im = partial(scale, comp_size_im, height)

    pool = Pool()
    pixels = product(range(height), range(width))
    points = ((re1+scale_re(x), im1+scale_im(y)) for y, x in pixels)
    return pool.map(f, points)
