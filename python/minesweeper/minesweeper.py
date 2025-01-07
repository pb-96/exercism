from typing import List, Tuple, Dict, Any

adjacent_moves: List[Tuple[int, int]] = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (1, 1),
]


def build_matrix(minefield: str) -> List[List[str]]:
    matrix = []
    for strs in minefield:
        this_line = []
        for chars in strs:
            this_line.append(chars)
        matrix.append(this_line)
    return matrix


def validate_pos(
    matrix: List[List[str]], row: int, col: int, cache: Dict[str, Any]
) -> int:
    position_count = 0
    for r, c in adjacent_moves:
        row_copy, col_copy = row + r, col + c
        cache_hit = (row_copy, col_copy) in cache
        if (
            cache_hit
            or (row_copy >= 0 and row_copy < len(matrix))
            and (col_copy >= 0 and col_copy < len(matrix[0]))
            and matrix[row_copy][col_copy] == "*"
        ):
            position_count += 1
            cache[(row_copy, col_copy)] = True
    return position_count


def annotate(minefield: List[str]):
    if not minefield:
        return []

    matrix = build_matrix(minefield)
    cache = {}
    first_line = len(matrix[0])
    for row, line in enumerate(matrix):
        if len(line) != first_line:
            raise ValueError("The board is invalid with current input.")
        for col, char in enumerate(line):
            if char == " ":
                position_count = validate_pos(matrix, row, col, cache)
                if position_count:
                    matrix[row][col] = str(position_count)
            elif char == "*":
                continue
            else:
                raise ValueError("The board is invalid with current input.")

    return ["".join(strs) for strs in matrix]


if __name__ == "__main__":
    test = ["X  * "]
    print(annotate(test))
