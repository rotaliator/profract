# cython: embedsignature=True
# cython: language_level=3
cimport cython
from cpython cimport array
from cython.parallel import parallel, prange


cdef unsigned char mandel_for(double re, double im, int max_dist=2**6, int max_iter=255) nogil:
    cdef double z_re = re
    cdef double z_im = im
    for i in range(max_iter):
        z_re, z_im = z_re*z_re - z_im*z_im + re, 2*z_re*z_im + im
        if ((z_re*z_re + z_im*z_im) >= max_dist):
            return i
    return max_iter

@cython.cdivision(True)
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
    cdef double re, im
    cdef unsigned char r
    cdef double pixel_size_re = comp_size_re / width
    cdef double pixel_size_im = comp_size_im / height

    while y < height:
        x = 0
        im = im1+y*pixel_size_im
        while x < width:
            index = x + y*width
            re = re1+x*pixel_size_re
            r = mandel_for(re, im)
            a[index] = r
            x = x + 1
        y = y + 1
    return a
