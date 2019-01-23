from __future__ import print_function
import sys
import time
import png
from mandel.pure_python import mandel

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
    try:
        outfile = sys.argv[1]
    except IndexError:
        outfile = "mandel.png"

    with Timer() as t:
        m = mandel(-2.0, -1.0, 1.0, 1.0, IMAGE_WIDTH, IMAGE_HEIGHT)
    print("Calculations took: {:.2f} sec".format( t.interval))

    save_array_as_png(m, outfile, IMAGE_WIDTH, IMAGE_HEIGHT)

if __name__ == '__main__':
    main()
