import numpy as np
import pytest
from PIL import Image

from src.pixel_cipher.cipher import (
    EncryptionMode,
    decrypt_image,
    encrypt_image,
)


def _make_image(tmp_path, name="in.png", size=(64, 48)):
    rng = np.random.default_rng(42)
    arr = rng.integers(0, 256, size=(size[1], size[0], 3), dtype=np.uint8)
    path = tmp_path / name
    Image.fromarray(arr, "RGB").save(path)
    return path, arr


@pytest.mark.parametrize("mode", [EncryptionMode.XOR, EncryptionMode.SHUFFLE, EncryptionMode.BOTH])
def test_roundtrip_recovers_original(tmp_path, mode):
    src, original = _make_image(tmp_path)
    enc = tmp_path / "enc.png"
    dec = tmp_path / "dec.png"
    encrypt_image(src, enc, "hunter2", mode=mode)
    decrypt_image(enc, dec, "hunter2", mode=mode)
    assert np.array_equal(np.array(Image.open(dec)), original)


def test_wrong_password_does_not_recover(tmp_path):
    src, original = _make_image(tmp_path)
    enc = tmp_path / "enc.png"
    dec = tmp_path / "dec.png"
    encrypt_image(src, enc, "correct-password")
    decrypt_image(enc, dec, "wrong-password")
    assert not np.array_equal(np.array(Image.open(dec)), original)


def test_encrypted_image_differs_from_original(tmp_path):
    src, original = _make_image(tmp_path)
    enc = tmp_path / "enc.png"
    encrypt_image(src, enc, "hunter2")
    assert not np.array_equal(np.array(Image.open(enc)), original)


def test_empty_password_rejected(tmp_path):
    src, _ = _make_image(tmp_path)
    with pytest.raises(ValueError):
        encrypt_image(src, tmp_path / "e.png", "")


def test_deterministic_output(tmp_path):
    src, _ = _make_image(tmp_path)
    e1 = tmp_path / "e1.png"
    e2 = tmp_path / "e2.png"
    encrypt_image(src, e1, "same-password")
    encrypt_image(src, e2, "same-password")
    assert np.array_equal(np.array(Image.open(e1)), np.array(Image.open(e2)))
