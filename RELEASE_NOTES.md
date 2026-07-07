# Pixel Cipher v1.0.0 — Initial Stable Release

First stable release of **Pixel Cipher**, a password-based image encryption library and CLI built on reversible pixel manipulation.

## Highlights
- 🔐 Two composable operations: **XOR keystream** and **deterministic pixel shuffle**
- 🎛️ Choose any combination via `--mode xor|shuffle|both`
- 🖥️ Clean CLI with password prompt (never echoed)
- 🧪 Parametrised `pytest` suite covering round-trips, wrong-password behavior, determinism, and input validation
- ⚙️ CI on Python 3.9 / 3.10 / 3.11 / 3.12
- 📦 Zero-boilerplate library API: `encrypt_image()` / `decrypt_image()`

## Usage
```bash
python main.py encrypt -i photo.jpg -o secret.png -p hunter2
python main.py decrypt -i secret.png -o restored.png -p hunter2
```
