"""Read the key/plaintext input file and write the result file."""

from pathlib import Path


def read_input(file_path: str) -> tuple[bytes, bytes]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}. Create input/input.txt first."
        )

    values = {}
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid input at line {line_number}: expected KEY=... or PLAINTEXT=...")
        name, value = line.split("=", 1)
        name = name.strip().upper()
        value = value.strip().replace(" ", "")
        if name not in {"KEY", "PLAINTEXT"}:
            raise ValueError(f"Unknown field '{name}' on line {line_number}.")
        if name in values:
            raise ValueError(f"Duplicate field '{name}' in input file.")
        try:
            values[name] = bytes.fromhex(value)
        except ValueError as exc:
            raise ValueError(f"{name} must contain valid hexadecimal bytes.") from exc

    missing = {"KEY", "PLAINTEXT"} - values.keys()
    if missing:
        raise ValueError(f"Missing input field(s): {', '.join(sorted(missing))}")

    if len(values["KEY"]) != 16:
        raise ValueError("KEY must be exactly 16 bytes (32 hexadecimal characters).")
    if len(values["PLAINTEXT"]) != 16:
        raise ValueError("PLAINTEXT must be exactly 16 bytes (32 hexadecimal characters).")

    return values["KEY"], values["PLAINTEXT"]


def write_output(file_path: str, content: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
