<h1 align="center">Pixel Cipher</h1>

<p align="center">
  <em>Image encryption using XOR keystream and pixel shuffling — with a friendly CLI, real tests, and CI.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="Python"/>
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License"/>
  <img src="https://github.com/nikunj-joshi-eth/pixel-cipher/actions/workflows/tests.yml/badge.svg" alt="Tests"/>
</p>

## See it in action

| Original | Encrypted |
|----------|-----------|
| ![original](assets/sample_original.png) | ![encrypted](assets/sample_encrypted.png) |

## Features

- **XOR keystream** — deterministic SHA-256-based keystream XORed with every pixel byte.
- **Pixel shuffle** — deterministic permutation of pixel positions using a seed.
- Reversible: decrypt with the same key/seed to recover the original exactly.
- Simple CLI, unit-tested with `pytest`, CI on Python 3.9 – 3.12.

## Installation

```bash
git clone https://github.com/nikunj-joshi-eth/pixel-cipher.git
cd pixel-cipher
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
# XOR encrypt / decrypt
pixel-cipher encrypt --algo xor --key "hunter2" -i photo.png -o enc.png
pixel-cipher decrypt --algo xor --key "hunter2" -i enc.png   -o out.png

# Pixel shuffle
pixel-cipher encrypt --algo shuffle --seed 42 -i photo.png -o enc.png
pixel-cipher decrypt --algo shuffle --seed 42 -i enc.png   -o out.png
```

## Testing

```bash
pytest -v
```

## Project structure

```
pixel-cipher/
├── src/pixel_cipher/
│   ├── __init__.py
│   ├── cipher.py        # XOR + shuffle primitives
│   └── cli.py           # CLI entry point
├── tests/test_cipher.py
├── examples/demo.py     # generates the before/after images in assets/
├── assets/              # sample images used in README
├── .github/workflows/tests.yml
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

## Security note

This is an educational project. XOR-with-a-keystream is only as strong as the
keystream's unpredictability, and pixel shuffling preserves the colour
histogram of the original image (so it leaks statistical structure). Do not
use this for real secrets — use vetted libraries like `cryptography` or
`libsodium` instead.

## License

MIT © Nikunj Joshi
