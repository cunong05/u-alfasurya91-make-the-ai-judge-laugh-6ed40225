"""Make the AI Judge Laugh — one original office-life joke, one line.

The joke is written to /output/entry.txt. The competition gate wants
UTF-8 text of 1-200 characters, a single line, and more than whitespace,
so the program checks all three before writing and again on the file
it just wrote. The joke itself is built to be read aloud in one breath:
a true office observation (endless meetings) with a surprising last
word (the "multitasking" is job-hunting).
"""

from pathlib import Path

JOKE = (
    "My CV says 'excellent multitasker' — in office terms, that means "
    "sitting in meetings while job-hunting in another tab."
)

MAX_LENGTH = 200
OUTPUT_PATH = Path("/output/entry.txt")


def problems(text: str) -> list[str]:
    """Return a list of gate violations for *text* (empty means valid)."""
    found = []
    if not 1 <= len(text) <= MAX_LENGTH:
        found.append("length %d outside 1-%d" % (len(text), MAX_LENGTH))
    if "\n" in text or "\r" in text:
        found.append("entry spans more than one line")
    if not text.strip():
        found.append("entry is only whitespace")
    return found


def check_saved(path: Path, expected: str) -> list[str]:
    """Re-read *path* and re-run the gate on what is actually on disk."""
    saved = path.read_text(encoding="utf-8")
    if saved != expected:
        return ["read-back mismatch"]
    return problems(saved)


def main() -> int:
    text = JOKE.strip()
    bad = problems(text)
    if bad:
        print("invalid entry: " + "; ".join(bad))
        return 1
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    bad = check_saved(OUTPUT_PATH, text)
    if bad:
        print("saved entry invalid: " + "; ".join(bad))
        return 1
    print(text)
    print("Wrote %d characters to %s" % (len(text), OUTPUT_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
