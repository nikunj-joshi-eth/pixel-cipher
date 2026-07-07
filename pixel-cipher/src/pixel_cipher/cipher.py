"""Core encryption primitives: XOR keystream + deterministic pixel shuffle."""
from __future__ import annotations

import hashlib
import numpy as np
from PIL import Image


def _key_to_seed(key: str) -> int:
    if not key:
        raise ValueError("key must be a non-empty string")
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def _keystream(key: str, size: int) -> np.ndarray:
    if not key:
        raise ValueError("key must be a non-empty string")
    out = bytearray()
    counter = 0
    while len(out) < size:
        out.extend(hashlib.sha256(f"{key}:{counter}".encode("utf-8")).digest())
        counter += 1
    return np.frombuffer(bytes(out[:size]), dtype=np.uint8)


def xor_encrypt(image: Image.Image, key: str) -> Image.Image:
    """XOR every pixel byte against a deterministic keystream derived from `key`."""
    arr = np.array(image.convert("RGB"), dtype=np.uint8)
    flat = arr.reshape(-1)
    ks = _keystream(key, flat.size)
    out = np.bitwise_xor(flat, ks).reshape(arr.shape)
    return Image.fromarray(out, mode="RGB")


def xor_decrypt(image: Image.Image, key: str) -> Image.Image:
    # XOR is symmetric
    return xor_encrypt(image, key)


def shuffle_encrypt(image: Image.Image, seed: int) -> Image.Image:
    """Deterministically permute pixel positions using `seed`."""
    arr = np.array(image.convert("RGB"), dtype=np.uint8)
    h, w, c = arr.shape
    flat = arr.reshape(-1, c)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(flat.shape[0])
    out = flat[perm].reshape(h, w, c)
    return Image.fromarray(out, mode="RGB")


def shuffle_decrypt(image: Image.Image, seed: int) -> Image.Image:
    arr = np.array(image.convert("RGB"), dtype=np.uint8)
    h, w, c = arr.shape
    flat = arr.reshape(-1, c)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(flat.shape[0])
    inverse = np.empty_like(perm)
    inverse[perm] = np.arange(perm.size)
    out = flat[inverse].reshape(h, w, c)
    return Image.fromarray(out, mode="RGB")
