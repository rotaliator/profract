# cython: embedsignature=True
# cython: language_level=3
# distutils: extra_compile_args = -fopenmp
# distutils: extra_link_args = -fopenmp
cimport cython
from cpython cimport array
from cython.parallel cimport parallel, prange


cdef unsigned char mandel_for(double re, double im, int max_dist=2**6, int max_iter=255) nogil:
    cdef double z_re = re
    cdef double z_im = im
    cdef int i
    cdef double re_sqr, im_sqr
    for i in range(max_iter):
        re_sqr = z_re*z_re
        im_sqr = z_im*z_im
        if ((re_sqr + im_sqr) >= max_dist):
            return i
        z_re, z_im = re_sqr - im_sqr + re, 2*z_re*z_im + im
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

    cdef int x, y, index
    cdef double re, im
    cdef unsigned char r
    cdef double pixel_size_re = comp_size_re / width
    cdef double pixel_size_im = comp_size_im / height

    for y in range(height):
        im = im1+y*pixel_size_im
        for x in range(width):
            index = x + y*width
            re = re1+x*pixel_size_re
            r = mandel_for(re, im)
            a[index] = r
    return a


@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef unsigned char[:] mandel_cython_multiproc(double re1, double im1, double re2, double im2, int width, int height):
    """
    Calculates iterations of mandelbrot set into array of doubles
    Cython optimized implementation - multicore version
    re1, im1 - upper left corner
    re2, im2 - lower right corner
    width, height - size of output image
    """
    cdef int size = width*height
    cdef double comp_size_re = re2 - re1
    cdef double comp_size_im = im2 - im1
    cdef unsigned char[:] a = cython.view.array(shape=(size,), itemsize=sizeof(unsigned char), format='B')

    cdef int x, y, index
    cdef double re, im
    cdef unsigned char r
    cdef double pixel_size_re = comp_size_re / width
    cdef double pixel_size_im = comp_size_im / height

    with cython.nogil, parallel():
        for y in prange(height):
            im = im1 + y*pixel_size_im
            for x in prange(width):
                index = x + y*width
                re = re1 + x*pixel_size_re
                r = mandel_for(re, im)
                a[index] = r

    return a
