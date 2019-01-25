from itertools import repeat
from cpython cimport array
import array


cdef float scale(float comp_size, int pixels, int pixel):
    return pixel*comp_size / pixels

cdef unsigned char mandel_for(float re, float im, int max_dist=2**6, int max_iter=255):
    cdef float z_re = re
    cdef float z_im = im
    for i in range(max_iter):
        z_re, z_im = z_re*z_re - z_im*z_im + re, 2*z_re*z_im + im
        if ((z_re*z_re + z_im*z_im) >= max_dist):
            return i
    return max_iter

cpdef unsigned char[:] mandel_cython(float re1, float im1, float re2, float im2, int width, int height):
    """
    Calculates iterations of mandelbrot set into array of floats
    pure Python reference implementation
    re1, im1 - upper left corner
    re2, im2 - lower right corner
    width, height - size of output image
    """
    cdef float comp_size_re = re2 - re1
    cdef float comp_size_im = im2 - im1
    cdef array.array a = array.array('B', repeat(255, width*height))

    cdef int x = 0
    cdef int y = 0
    cdef int index = 0

    while y < height:
        x = 0
        while x < width:
            index = x + y*width
            r = mandel_for(re1+scale(comp_size_re, width, x), im1+scale(comp_size_im, height, y))
            a[index] = r
            x = x + 1
        y = y + 1
    return a