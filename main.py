#!/usr/bin/env python3
"""Famous Last Words: The Funniest Epitaph.

Writes one one-line tombstone epitaph (famous last words, <= 150 chars)
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The line: a dying plea for "one more minute" answered with "forever" --
the stonecutter's twist is that the request was granted literally.
"""

import os
import stat


def build_epitaph():
    plea = "I asked for one more minute."
    answer = "They gave me forever."
    return plea + " " + answer


def check_gate(text):
    """Mirror the sealed gate: UTF-8, 1-150 chars, not only whitespace,
    exactly one line, no trailing newline (the file is the line itself)."""
    encoded = text.encode("utf-8")
    if not (1 <= len(text) <= 150):
        raise ValueError("epitaph must be 1-150 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("epitaph must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("epitaph must be a single line")
    if text != text.strip():
        raise ValueError("epitaph must not start or end with whitespace")
    return encoded


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = build_epitaph()
    data = check_gate(text)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    # Round-trip check: what the grader reads must be byte-identical.
    with open(path, "rb") as handle:
        if handle.read() != data:
            raise RuntimeError("entry.txt round-trip mismatch")
    print("wrote %s (%d chars)" % (path, len(text)))


if __name__ == "__main__":
    main()
