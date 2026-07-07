"""Command-line interface for pixel-cipher."""
from __future__ import annotations

import argparse
import sys
from PIL import Image

from .cipher import xor_encrypt, xor_decrypt, shuffle_encrypt, shuffle_decrypt


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="pixel-cipher",
        description="Encrypt or decrypt an image using XOR keystream or pixel shuffling.",
    )
    p.add_argument("mode", choices=["encrypt", "decrypt"])
    p.add_argument("--algo", choices=["xor", "shuffle"], default="xor")
    p.add_argument("--input", "-i", required=True, help="input image path")
    p.add_argument("--output", "-o", required=True, help="output image path")
    p.add_argument("--key", help="secret string (required for --algo xor)")
    p.add_argument("--seed", type=int, help="integer seed (required for --algo shuffle)")
    args = p.parse_args(argv)

    img = Image.open(args.input)

    if args.algo == "xor":
        if not args.key:
            p.error("--key is required for --algo xor")
        fn = xor_encrypt if args.mode == "encrypt" else xor_decrypt
        out = fn(img, key=args.key)
    else:
        if args.seed is None:
            p.error("--seed is required for --algo shuffle")
        fn = shuffle_encrypt if args.mode == "encrypt" else shuffle_decrypt
        out = fn(img, seed=args.seed)

    out.save(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
