import numpy as np
import pytest
from PIL import Image

from pixel_cipher.cipher import (
    xor_encrypt,
    xor_decrypt,
    shuffle_encrypt,
    shuffle_decrypt,
)


def _sample_image():
    rng = np.random.default_rng(42)
    arr = rng.integers(0, 256, size=(16, 16, 3), dtype=np.uint8)
    return Image.fromarray(arr, mode="RGB")


def test_xor_roundtrip():
    img = _sample_image()
    enc = xor_encrypt(img, key="hunter2")
    dec = xor_decrypt(enc, key="hunter2")
    assert np.array_equal(np.array(img), np.array(dec))


def test_xor_wrong_key_differs():
    img = _sample_image()
    enc = xor_encrypt(img, key="hunter2")
    dec = xor_decrypt(enc, key="wrong")
    assert not np.array_equal(np.array(img), np.array(dec))


def test_shuffle_roundtrip():
    img = _sample_image()
    enc = shuffle_encrypt(img, seed=1234)
    dec = shuffle_decrypt(enc, seed=1234)
    assert np.array_equal(np.array(img), np.array(dec))


def test_shuffle_wrong_seed_differs():
    img = _sample_image()
    enc = shuffle_encrypt(img, seed=1234)
    dec = shuffle_decrypt(enc, seed=9999)
    assert not np.array_equal(np.array(img), np.array(dec))


def test_xor_deterministic():
    img = _sample_image()
    a = xor_encrypt(img, key="k")
    b = xor_encrypt(img, key="k")
    assert np.array_equal(np.array(a), np.array(b))


def test_shuffle_deterministic():
    img = _sample_image()
    a = shuffle_encrypt(img, seed=7)
    b = shuffle_encrypt(img, seed=7)
    assert np.array_equal(np.array(a), np.array(b))


def test_xor_empty_key_rejected():
    img = _sample_image()
    with pytest.raises(ValueError):
        xor_encrypt(img, key="")
