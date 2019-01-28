from multiprocessing import Pool
# from multiprocessing.pool import ThreadPool as Pool
# For multithreaded version just uncomment line above.
# It is cpu bound task, so it should not speed up calculations
# [in fact it will slow them ;) ]
from .pure_python import mandel_for

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
    pixel_size_re = comp_size_re / width
    pixel_size_im = comp_size_im / height

    pool = Pool()
    pixels = product(range(height), range(width))
    points = ((re1 + x*pixel_size_re, im1 + y*pixel_size_im) for y, x in pixels)
    return array('B', pool.map(f, points))
