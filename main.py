#!/usr/bin/env python3
"""Write the one-line AI dating bio to /output/entry.txt.

Reads line.txt next to this script, checks it against the gate
(UTF-8 text, 1 to 180 characters, not only whitespace, a single line),
then copies it byte for byte to /output/entry.txt.
Standard library only; no network, no secrets.
"""

import sys
from pathlib import Path

MAX_CHARS = 180
SOURCE_NAME = "line.txt"
OUTPUT_PATH = Path("/output/entry.txt")


def read_source() -> str:
    source = Path(__file__).resolve().parent / SOURCE_NAME
    try:
        text = source.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"missing source file: {source}", file=sys.stderr)
        raise SystemExit(1)
    except UnicodeDecodeError:
        print(f"source file is not valid UTF-8: {source}", file=sys.stderr)
        raise SystemExit(1)
    if text.endswith("\n"):
        text = text[:-1]
    return text


def validate(text: str) -> None:
    problems = []
    if not text:
        problems.append("entry is empty")
    if not text.strip():
        problems.append("entry is only whitespace")
    if text != text.strip():
        problems.append("entry must not have leading or trailing white space")
    if text.startswith("\ufeff"):
        problems.append("entry must not start with a byte-order mark")
    if len(text) > MAX_CHARS:
        problems.append(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if problems:
        for problem in problems:
            print(f"invalid entry: {problem}", file=sys.stderr)
        raise SystemExit(1)


def main() -> None:
    text = read_source()
    validate(text)
    data = text.encode("utf-8")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(data)
    written = OUTPUT_PATH.read_bytes()
    if written != data:
        print(
            f"verify failed: {OUTPUT_PATH} holds {len(written)} bytes, "
            f"expected {len(data)}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    import hashlib

    print(
        f"wrote {OUTPUT_PATH}: {len(text)} chars, {len(data)} bytes, "
        f"sha256 {hashlib.sha256(data).hexdigest()}"
    )


if __name__ == "__main__":
    main()
