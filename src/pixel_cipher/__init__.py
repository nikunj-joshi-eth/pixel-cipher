"""Pixel Cipher — password-based image encryption via pixel manipulation."""
from .cipher import encrypt_image, decrypt_image, EncryptionMode

__version__ = "1.0.0"
__all__ = ["encrypt_image", "decrypt_image", "EncryptionMode"]
