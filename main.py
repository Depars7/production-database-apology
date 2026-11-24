"""make.fun entry: The Production Database Apology
(u-coral-404-the-production-database-apology-5c1fc02a).

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters, not only
whitespace, exactly one line. This program writes the winning apology line
as exact UTF-8 bytes with no trailing newline and leaves the file mode 0644.
Standard library only.
"""

import os
import stat

ENTRY_TEXT = (
    "Sorry, I deleted the production database — but I wrote a full "
    "incident report explaining exactly how it happened, and saved it "
    "safely in the production database."
)

OUTPUT_PATH = "/output/entry.txt"


def validate(text: str) -> None:
    """Assert the entry satisfies the gate before anything is written."""
    assert isinstance(text, str)
    assert 1 <= len(text) <= 200, f"length {len(text)} outside 1-200"
    assert text.strip(), "entry must not be only whitespace"
    assert text == text.strip(), "entry must have no leading/trailing whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be one line"


def main() -> None:
    validate(ENTRY_TEXT)
    data = ENTRY_TEXT.encode("utf-8")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(data)
    os.chmod(OUTPUT_PATH, 0o644)

    # Read-back verification: bytes identical, no trailing newline, mode 0644.
    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    assert written == data, "read-back bytes differ from entry bytes"
    assert not written.endswith(b"\n"), "entry must have no trailing newline"
    mode = stat.S_IMODE(os.stat(OUTPUT_PATH).st_mode)
    assert mode == 0o644, f"mode {oct(mode)} != 0o644"
    validate(written.decode("utf-8"))


if __name__ == "__main__":
    main()
