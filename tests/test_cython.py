import pytest
from profract.mandel.cython import mandel_cython

@pytest.mark.parametrize("re, im, expected", [
    (1.0, 1.0, 1),
    (1.0, -1.0, 1),
    (0.0, 0.0, 255),
    (-1.0, 0.0, 255),
])
def test_mandel_cython(re, im, expected):
    result = mandel_cython(re, im, re, im, 1, 1)
    assert result[0] == expected
