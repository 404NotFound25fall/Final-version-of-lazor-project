
# /mnt/data/parse_bff_demo.py
from __future__ import annotations
import sys
from lazor_core import parse_bff, Board

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_bff_demo.py <path/to/board.bff>")
        sys.exit(1)
    path = sys.argv[1]
    spec = parse_bff(path)
    board = Board.from_bffspec(spec)
    print(board.summary())

if __name__ == "__main__":
    main()
