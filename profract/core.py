from __future__ import print_function
import sys
import time
import png
from mandel.pure_python import mandel_classic
from mandel.pure_python import mandel_functional
from mandel.pure_python_multiproc import mandel as mandel_multiproc
from mandel.cython import mandel_cython

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

def save_array_as_png(array, filename, width, height):
    writer = png.Writer(width=width, height=height, greyscale=True)
    with open(filename, "wb") as f:
        writer.write_array(f, array)

def main():
    """
    with Timer() as t:
        m = mandel_classic(-2.0, -1.0, 1.0, 1.0, IMAGE_WIDTH, IMAGE_HEIGHT)
    print("Single proc calculations took: {:.2f} sec".format( t.interval))
    save_array_as_png(m, "mandel_classic.png", IMAGE_WIDTH, IMAGE_HEIGHT)

    with Timer() as t:
        m = mandel_functional(-2.0, -1.0, 1.0, 1.0, IMAGE_WIDTH, IMAGE_HEIGHT)
    print("Single proc higher order functions calculations took: {:.2f} sec".format( t.interval))
    save_array_as_png(m, "mandel_functional.png", IMAGE_WIDTH, IMAGE_HEIGHT)
    """
    with Timer() as t:
        m = mandel_multiproc(-2.0, -1.0, 1.0, 1.0, IMAGE_WIDTH, IMAGE_HEIGHT)
    print("Multi proc calculations took: {:.2f} sec".format( t.interval))
    save_array_as_png(m, "mandel_multiproc.png", IMAGE_WIDTH, IMAGE_HEIGHT)

    with Timer() as t:
        m = mandel_cython(-2.0, -1.0, 1.0, 1.0, IMAGE_WIDTH, IMAGE_HEIGHT)
    print("Cython calculations took: {:.2f} sec".format( t.interval))
    save_array_as_png(m, "mandel_cython.png", IMAGE_WIDTH, IMAGE_HEIGHT)


if __name__ == '__main__':
    main()
