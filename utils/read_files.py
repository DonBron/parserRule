import csv
import logging
from pathlib import Path

log = logging.getLogger(__name__)


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
            if len(row) != 3:
                log.warning(f'!= 3 | {row}')
            rows.append(row)
    return rows
