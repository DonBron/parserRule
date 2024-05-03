import csv
from pathlib import Path


def read_csv(
    file_path: Path | str,
    newline: str = '',
    encoding: str = 'utf-8',
    delimiter: str = ';',
    quotechar: str = '"',
) -> list[list[str]]:
    rows = []
    with open(file_path, newline=newline, encoding=encoding) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            rows.append(row)
    return rows
