import setuptools
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="Profract",
    version="0.1",
    ext_modules=cythonize(
        ["profract/mandel/mandel_cython.pyx"],
        compiler_directives={"language_level": 3}),
)
