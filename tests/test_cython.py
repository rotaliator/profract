import pytest
try:
    from profract.mandel.mandel_cython import mandel_cython, mandel_cython_multiproc
    CYTHON = True
except:
    CYTHON = False

pytestmark = pytest.mark.skipif(not CYTHON, reason="No cython, not test")

@pytest.mark.parametrize("re, im, expected", [
    (1.0, 1.0, 1),
    (1.0, -1.0, 1),
    (0.0, 0.0, 255),
    (-1.0, 0.0, 255),
])
def test_mandel_cython(re, im, expected):
    result = mandel_cython(re, im, re, im, 1, 1)
    assert result[0] == expected

@pytest.mark.parametrize("re, im, expected", [
    (1.0, 1.0, 1),
    (1.0, -1.0, 1),
    (0.0, 0.0, 255),
    (-1.0, 0.0, 255),
])
def test_mandel_cython_multiproc(re, im, expected):
    result = mandel_cython_multiproc(re, im, re, im, 1, 1)
    assert result[0] == expected

def test_for_profiling():
    result = mandel_cython(-2.0, -1.0, 1.0, 1.0, 1600, 1200)
    result_len = len(result)
    assert result_len == 1600*1200
    assert result[0] == 1
    assert result[result_len-1] == 1
