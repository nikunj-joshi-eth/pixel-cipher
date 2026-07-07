"""Entry point so users can run: python main.py encrypt -i in.png -o out.png"""
import sys
from src.pixel_cipher.cli import main

if __name__ == "__main__":
    sys.exit(main())
