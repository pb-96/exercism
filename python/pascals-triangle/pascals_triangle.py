from typing import List
import sys

DEFAULT = [
    [1],
    [1, 1],
    [1, 2, 1],
]


def pad_rows(row_count: int) -> List[List[int]]:
    start_from = len(DEFAULT)
    result = [*DEFAULT]
    for row in range(start_from, row_count):
        default = [1 for _ in range(row + 1)]
        for idx in range(1, len(default)):
            last_added = result[-1]
            default[idx] = sum(last_added[idx - 1 : idx + 1])
        result.append(default)
    return result


def rows(row_count: int):
    if row_count < 0:
        raise ValueError("number of rows is negative")
    elif row_count > sys.getrecursionlimit():
        raise RecursionError("maximum recursion depth exceeded")
    elif row_count == 0:
        return []
    elif row_count <= len(DEFAULT):
        return DEFAULT[:row_count]

    return pad_rows(row_count)


if __name__ == "__main__":
    print(rows(6))
