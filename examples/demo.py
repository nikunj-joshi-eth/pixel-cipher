"""Quick demo: encrypt then decrypt an image."""
from pathlib import Path

from src.pixel_cipher import decrypt_image, encrypt_image

HERE = Path(__file__).parent
sample = HERE / "sample.png"
encrypted = HERE / "sample.encrypted.png"
recovered = HERE / "sample.recovered.png"

if not sample.exists():
    from PIL import Image
    import numpy as np
    Image.fromarray(np.random.default_rng(0).integers(0, 256, (128, 128, 3), dtype=np.uint8), "RGB").save(sample)

encrypt_image(sample, encrypted, password="hunter2")
decrypt_image(encrypted, recovered, password="hunter2")
print("Encrypted →", encrypted)
print("Recovered →", recovered)
