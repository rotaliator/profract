import pytest
from profract.mandel.pure_python import mandel_for

@pytest.mark.parametrize("re, im, expected", [
    (1.0, 1.0, 2),
    (1.0, -1.0, 2),
    (0.0, 0.0, 255),
    (-1.0, 0.0, 255),
])
def test_mandel_for(re, im, expected):
    assert mandel_for(re, im, max_iter=255) == expected
