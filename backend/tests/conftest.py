from pathlib import Path


def read_file(file_name: str) -> str:
    path = Path("./tests/data")
    file_path = path / file_name
    with open(file_path, "r") as file:
        return file.read()
