#!/usr/bin/env python3
"""news-image-20261126 entrypoint (stdlib only).

Copies the pre-rendered front page (entry.png, drawn at build time with
Pillow) to $MAKEFUN_OUTPUT_DIR/entry.png and checks the PNG magic bytes.
No rendering happens here: the grading image has no Pillow, no DejaVu
fonts and no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(SRC, "rb") as f:
        head = f.read(8)
    if head != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if os.path.getsize(SRC) > 1048576:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
