from pytest import approx
import distogram


def test_update():
    h = distogram.Distogram(bin_count=3)

    # fill histogram
    h = distogram.update(h, 23)
    assert h.bins == [(23, 1)]
    h = distogram.update(h, 28)
    assert h.bins == [(23, 1), (28, 1)]
    h = distogram.update(h, 16)
    assert h.bins == [(16, 1), (23, 1), (28, 1)]

    # update count on existing value
    h = distogram.update(h, 23)
    assert h.bins == [(16, 1), (23, 2), (28, 1)]
    h = distogram.update(h, 28)
    assert h.bins == [(16, 1), (23, 2), (28, 2)]
    h = distogram.update(h, 16)
    assert h.bins == [(16, 2), (23, 2), (28, 2)]

    # merge values
    h = distogram.update(h, 26)
    assert h.bins[0] == (16, 2)
    assert h.bins[1] == (23, 2)
    assert h.bins[2][0] == approx(27.33333)
    assert h.bins[2][1] == 3
