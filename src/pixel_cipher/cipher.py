"""Core image encryption/decryption using pixel manipulation.

Two composable operations, both keyed by a password:
  1. XOR    — per-channel byte XOR with a keystream derived from the password.
  2. SHUFFLE — deterministic pixel-position shuffle using a seeded PRNG.

Both operations are perfectly reversible when given the same password.
"""
from __future__ import annotations

import hashlib
from enum import Flag, auto
from pathlib import Path
from typing import Union

import numpy as np
from PIL import Image


class EncryptionMode(Flag):
    XOR = auto()
    SHUFFLE = auto()
    BOTH = XOR | SHUFFLE


PathLike = Union[str, Path]


def _keystream(password: str, length: int) -> np.ndarray:
    """Derive a deterministic byte keystream of `length` bytes from the password."""
    seed = hashlib.sha256(password.encode("utf-8")).digest()
    out = bytearray()
    counter = 0
    while len(out) < length:
        block = hashlib.sha256(seed + counter.to_bytes(8, "big")).digest()
        out.extend(block)
        counter += 1
    return np.frombuffer(bytes(out[:length]), dtype=np.uint8)


def _seed_int(password: str) -> int:
    return int.from_bytes(hashlib.sha256(password.encode("utf-8")).digest()[:8], "big")


def _permutation(password: str, n: int) -> np.ndarray:
    rng = np.random.default_rng(_seed_int(password))
    return rng.permutation(n)


def _apply_xor(arr: np.ndarray, password: str) -> np.ndarray:
    flat = arr.reshape(-1)
    key = _keystream(password, flat.size)
    return np.bitwise_xor(flat, key).reshape(arr.shape)


def _apply_shuffle(arr: np.ndarray, password: str, reverse: bool) -> np.ndarray:
    h, w = arr.shape[:2]
    n = h * w
    perm = _permutation(password, n)
    flat_pixels = arr.reshape(n, -1)
    if reverse:
        inv = np.empty_like(perm)
        inv[perm] = np.arange(n)
        flat_pixels = flat_pixels[inv]
    else:
        flat_pixels = flat_pixels[perm]
    return flat_pixels.reshape(arr.shape)


def _load(path: PathLike) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    return np.array(img, dtype=np.uint8)


def _save(arr: np.ndarray, path: PathLike) -> None:
    Image.fromarray(arr, mode="RGB").save(path)


def encrypt_image(
    input_path: PathLike,
    output_path: PathLike,
    password: str,
    mode: EncryptionMode = EncryptionMode.BOTH,
) -> None:
    """Encrypt `input_path` with `password` and write to `output_path`."""
    if not password:
        raise ValueError("password must be a non-empty string")
    arr = _load(input_path)
    if EncryptionMode.SHUFFLE in mode:
        arr = _apply_shuffle(arr, password, reverse=False)
    if EncryptionMode.XOR in mode:
        arr = _apply_xor(arr, password)
    _save(arr, output_path)


def decrypt_image(
    input_path: PathLike,
    output_path: PathLike,
    password: str,
    mode: EncryptionMode = EncryptionMode.BOTH,
) -> None:
    """Reverse `encrypt_image` — same password + mode restores the original."""
    if not password:
        raise ValueError("password must be a non-empty string")
    arr = _load(input_path)
    if EncryptionMode.XOR in mode:
        arr = _apply_xor(arr, password)  # XOR is self-inverse
    if EncryptionMode.SHUFFLE in mode:
        arr = _apply_shuffle(arr, password, reverse=True)
    _save(arr, output_path)
