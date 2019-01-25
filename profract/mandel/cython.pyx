# cython: embedsignature=True
# cython: language_level=3
cimport cython
from cpython cimport array


@cython.cdivision(True)
cdef double scale(double comp_size, int pixels, int pixel) except *:
    return pixel*comp_size / pixels

cdef unsigned char mandel_for(double re, double im, int max_dist=2**6, int max_iter=255):
    cdef double z_re = re
    cdef double z_im = im
    for i in range(max_iter):
        z_re, z_im = z_re*z_re - z_im*z_im + re, 2*z_re*z_im + im
        if ((z_re*z_re + z_im*z_im) >= max_dist):
            return i
    return max_iter

@cython.boundscheck(False)
cpdef unsigned char[:] mandel_cython(double re1, double im1, double re2, double im2, int width, int height):
    """
    Calculates iterations of mandelbrot set into array of doubles
    Cython optimized implementation
    re1, im1 - upper left corner
    re2, im2 - lower right corner
    width, height - size of output image
    """
    cdef int size = width*height
    cdef double comp_size_re = re2 - re1
    cdef double comp_size_im = im2 - im1
    cdef unsigned char[:] a = cython.view.array(shape=(size,), itemsize=sizeof(unsigned char), format='B')

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
