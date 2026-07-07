"""Command-line interface for pixel-cipher."""
from __future__ import annotations

import argparse
import getpass
import sys

from .cipher import EncryptionMode, decrypt_image, encrypt_image


def _parse_mode(name: str) -> EncryptionMode:
    return {
        "xor": EncryptionMode.XOR,
        "shuffle": EncryptionMode.SHUFFLE,
        "both": EncryptionMode.BOTH,
    }[name]


def _get_password(args: argparse.Namespace) -> str:
    if args.password:
        return args.password
    return getpass.getpass("Password: ")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pixel-cipher",
        description="Encrypt or decrypt images via reversible pixel manipulation.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    for name, help_text in (("encrypt", "Encrypt an image"), ("decrypt", "Decrypt an image")):
        sp = sub.add_parser(name, help=help_text)
        sp.add_argument("-i", "--input", required=True, help="Input image path")
        sp.add_argument("-o", "--output", required=True, help="Output image path")
        sp.add_argument("-p", "--password", help="Password (prompted if omitted)")
        sp.add_argument(
            "-m", "--mode", default="both", choices=["xor", "shuffle", "both"],
            help="Which operation(s) to apply (default: both)",
        )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    password = _get_password(args)
    mode = _parse_mode(args.mode)
    action = encrypt_image if args.command == "encrypt" else decrypt_image
    action(args.input, args.output, password, mode=mode)
    print(f"[pixel-cipher] {args.command}ed → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
