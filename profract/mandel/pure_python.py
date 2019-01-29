from itertools import repeat, product
from functools import partial
from array import array


def mandel_for(re, im, max_dist=2**6, max_iter=255):
    z_re, z_im = re, im
    for i in range(max_iter):
        re_sqr = z_re*z_re
        im_sqr = z_im*z_im
        if ((re_sqr + im_sqr) >= max_dist):
            return i
        z_re, z_im = re_sqr - im_sqr + re, 2*z_re*z_im + im
    return max_iter

def mandel_classic(re1, im1, re2, im2, width, height):
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
    pixel_size_re = comp_size_re / width
    pixel_size_im = comp_size_im / height

    for y, x in product(range(height), range(width)):
        index = x + y*width
        a[index] = mandel_for(re1 + x*pixel_size_re, im1 + y*pixel_size_im)
    return a

def f(re_im):
    re, im = re_im
    return mandel_for(re, im)
