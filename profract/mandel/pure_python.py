from itertools import repeat, product
from functools import partial
from array import array

def scale(comp_size, pixel_size, pixel):
    return pixel*comp_size / pixel_size

def mandel_for(re, im, max_dist=2**6, max_iter=255):
    z_re, z_im = re, im
    for i in range(max_iter):
        z_re, z_im = z_re*z_re - z_im*z_im + re, 2*z_re*z_im + im
        if ((z_re*z_re + z_im*z_im) >= max_dist):
            return i
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
    scale_re = partial(scale, comp_size_re, width)
    scale_im = partial(scale, comp_size_im, height)
    for y, x in product(range(height), range(width)):
        index = x + y*width
        a[index] = mandel_for(re1+scale_re(x), im1+scale_im(y))
    return a

def f(re_im):
    re, im = re_im
    return mandel_for(re, im)

def mandel_functional(re1, im1, re2, im2, width, height):
    """
    Calculates iterations of mandelbrot set into array of floats
    pure Python reference implementation
    re1, im1 - upper left corner
    re2, im2 - lower right corner
    width, height - size of output image
    """
    comp_size_re = re2 - re1
    comp_size_im = im2 - im1
    scale_re = partial(scale, comp_size_re, width)
    scale_im = partial(scale, comp_size_im, height)
    pixels = product(range(height), range(width))
    points = ((re1+scale_re(x), im1+scale_im(y)) for y, x in pixels)

    return array('B', map(f, points))
