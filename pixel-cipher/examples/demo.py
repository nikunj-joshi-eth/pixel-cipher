"""Generate before/after sample images in assets/."""
from pathlib import Path
import numpy as np
from PIL import Image
from pixel_cipher.cipher import xor_encrypt

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

rng = np.random.default_rng(0)
h, w = 128, 128
grad = np.zeros((h, w, 3), dtype=np.uint8)
grad[..., 0] = np.linspace(0, 255, w, dtype=np.uint8)[None, :]
grad[..., 1] = np.linspace(0, 255, h, dtype=np.uint8)[:, None]
grad[..., 2] = 128
img = Image.fromarray(grad, mode="RGB")
img.save(ASSETS / "sample_original.png")

enc = xor_encrypt(img, key="demo-key")
enc.save(ASSETS / "sample_encrypted.png")

print("wrote assets/sample_original.png and assets/sample_encrypted.png")
