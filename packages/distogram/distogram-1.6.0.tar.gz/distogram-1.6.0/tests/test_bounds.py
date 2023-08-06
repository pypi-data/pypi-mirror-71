import distogram
import random


def test_bounds():
    normal = [random.normalvariate(0.0, 1.0) for _ in range(10000)]
    h = distogram.Distogram()

    for i in normal:
        h = distogram.update(h, i)

    dmin, dmax = distogram.bounds(h)
    assert dmin == min(normal)
    assert dmax == max(normal)
