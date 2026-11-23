#!/usr/bin/env python3
"""Entry point for the 23 November 2026 news image.

The picture itself is drawn by draw.py and committed as entry.png; this
program only places that file where the grader expects it. It checks the
file really is a PNG, then writes it to the output directory in one
atomic step so a half-written file can never be judged.
"""
import os
import shutil
import sys
import tempfile

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def entry_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def output_dir():
    # The grader sets MAKEFUN_OUTPUT_DIR; /output is its usual value.
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    source = entry_path()
    with open(source, "rb") as handle:
        magic = handle.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print(f"entry.png is not a PNG: {source}", file=sys.stderr)
        return 1

    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")

    # Copy through a temp file in the same directory, then rename, so the
    # destination is either the whole image or the previous one.
    fd, tmp = tempfile.mkstemp(prefix=".entry-", dir=target_dir)
    try:
        with os.fdopen(fd, "wb") as out:
            with open(source, "rb") as src:
                shutil.copyfileobj(src, out)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    print(f"wrote {target} ({os.path.getsize(target)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
