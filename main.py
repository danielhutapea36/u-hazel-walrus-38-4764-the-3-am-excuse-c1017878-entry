#!/usr/bin/env python3
"""The 3 AM Excuse — make.fun entry.

Writes one line to /output/entry.txt: the excuse a hardware wallet
gives for refusing to sign a transaction at 3 AM.

The joke: the wallet's secure element treats 3 AM as a filing
category of its own — "you, but sleep-deprived" — a different,
untrustworthy person it refuses to sign for. The hour itself is
the reason, not a dead battery or a firmware update: the device
protects the owner from the sleep-deprived version of the owner.

Deterministic by design: standard library only, no network, no
randomness, no clock reads. Every run writes byte-identical output.
"""

import os
import sys

# The excuse in two clauses, joined with a single space. The first
# clause sets up the wallet's filing system; the second delivers the
# refusal. Neither clause is funny alone — the turn is the joke.
_CLAUSES = (
    "My secure element files 3 AM under 'you, but sleep-deprived' \u2014",
    "and it won't sign for that person.",
)

# Competition ceiling for the single line (kit RULES.txt gate: 1-200).
MAX_LINE_CHARS = 200


def build_line() -> str:
    """Assemble the one-line excuse from its clauses.

    The result must be exactly one line: a stray newline would
    silently break the entry format, so fail loudly instead of
    writing a malformed file.
    """
    line = " ".join(_CLAUSES)
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    if not line.strip():
        raise ValueError("line must not be only white space")
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8.

    Reads the file back after writing and fails loudly if the bytes
    on disk differ from the line — a partial write must never pass
    as a finished entry.
    """
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != line.encode("utf-8"):
        raise ValueError("entry.txt bytes differ from the built line")


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
