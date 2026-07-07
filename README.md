<div align="center">

# 🖼️ Pixel Cipher

**Password-based image encryption via reversible pixel manipulation.**

Encrypt any image so its pixels are visually scrambled, then decrypt it back to a byte-perfect original — all with a single password.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Tests](https://github.com/nikunj-joshi-eth/pixel-cipher/actions/workflows/tests.yml/badge.svg)
![License](https://img.shields.io/github/license/nikunj-joshi-eth/pixel-cipher)
![Release](https://img.shields.io/github/v/release/nikunj-joshi-eth/pixel-cipher)
![Stars](https://img.shields.io/github/stars/nikunj-joshi-eth/pixel-cipher?style=social)

</div>

---

## ✨ Features

- 🔐 **XOR keystream** — every byte XOR-ed with a SHA-256-derived keystream
- 🔀 **Pixel shuffle** — deterministic permutation seeded from the password
- 🎛️ Use either operation alone, or both stacked (`--mode both`, default)
- ↩️ Perfectly reversible: same password → byte-identical original
- 🚫 Wrong password → visually unrecognisable output (no accidental recovery)
- 🖥️ Clean CLI with hidden password prompt
- 🧪 Full `pytest` suite; CI on Python 3.9 – 3.12
- 📦 Only depends on `numpy` and `Pillow`

---

## 🚀 Quick start

```bash
git clone https://github.com/nikunj-joshi-eth/pixel-cipher.git
cd pixel-cipher
pip install -r requirements.txt
```

### CLI

```bash
# Encrypt (password prompt is hidden)
python main.py encrypt -i cat.png -o cat.enc.png

# Decrypt back to the original
python main.py decrypt -i cat.enc.png -o cat.out.png

# Pick an operation
python main.py encrypt -i cat.png -o cat.enc.png -m shuffle
python main.py encrypt -i cat.png -o cat.enc.png -m xor
```

### Library

```python
from pixel_cipher import encrypt_image, decrypt_image, EncryptionMode

encrypt_image("cat.png", "cat.enc.png", password="hunter2")
decrypt_image("cat.enc.png", "cat.out.png", password="hunter2")

# Only shuffle pixel positions (keeps the color histogram intact)
encrypt_image("cat.png", "cat.shuf.png", password="hunter2",
              mode=EncryptionMode.SHUFFLE)
```

---

## 🧠 How it works

Every image is a 3-D array of `uint8` pixel values `(H × W × 3)`. Pixel Cipher applies one or two reversible operations, both keyed by the password:

| Operation | What it does | Why it's reversible |
|-----------|--------------|---------------------|
| **XOR**     | Each byte is XOR-ed with a pseudo-random keystream derived from `SHA-256(password)` | XOR is self-inverse: `x ⊕ k ⊕ k = x` |
| **SHUFFLE** | Pixel positions are permuted with a `numpy` PRNG seeded by the password | Store the permutation → apply its inverse on decrypt |

Both operations are 100% deterministic, so the same password always produces the same output.

> ⚠️ **Security note.** This is a *learning* / *portfolio* project demonstrating pixel manipulation, not a production-grade cipher. It is not IND-CPA secure and should not be used to protect sensitive data — reach for AES-GCM (via `cryptography`) for real workloads.

---

## 🧪 Running tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

The suite covers: round-trip recovery for every mode, wrong-password behavior, deterministic output, and input validation.

---

## 📂 Project structure

```text
pixel-cipher/
├── src/pixel_cipher/
│   ├── cipher.py         # encrypt / decrypt core
│   └── cli.py            # argparse-based CLI
├── tests/                # pytest suite
├── examples/demo.py      # generate + encrypt + decrypt a sample image
├── .github/workflows/    # CI (multi-version pytest)
├── main.py               # CLI launcher
└── README.md
```

---

## 🗺️ Roadmap

- [ ] AES-GCM mode for real confidentiality
- [ ] Batch encrypt an entire folder
- [ ] Streamlit demo with before/after preview
- [ ] Support for PNG alpha channels and grayscale images

---

## 📜 License

MIT © [Nikunj Joshi](https://github.com/nikunj-joshi-eth)
