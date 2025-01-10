from typing import List, Tuple, Union, Set


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y

    def add_tuple(self, positions: Tuple[int, int]) -> "Point":
        row, col = positions
        y = self.y + col
        x = self.x + row
        return Point(x=x, y=y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


class WordSearch:
    def __init__(self, puzzle: List[List[str]]) -> None:
        self.puzzle = puzzle
        self.search_points = [
            (-1, 1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]

    def valid_point(self, point: Point):
        return (
            point.x >= 0
            and point.x < len(self.puzzle[0])
            and point.y >= 0
            and point.y < len(self.puzzle)
        )

    def peek_next(
        self, s: Point, potential_positions: Tuple[int, int]
    ) -> Union[None, Tuple[Point, str]]:
        new_point = s.add_tuple(potential_positions)

        if not self.valid_point(new_point):
            return (None, None)

        next_char = self.puzzle[new_point.y][new_point.x]
        return next_char, new_point

    def non_rec_dfs(
        self,
        next_point: Point,
        potential_positions: Tuple[int, int],
        search_word: str,
        ptr: int
    ) -> Union[Point, None]:
        built = search_word[ptr]
        while ptr < len(search_word) - 1:
            next_char, next_point = self.peek_next(next_point, potential_positions)
            if next_char is None or next_char != search_word[ptr + 1]:
                return None
            ptr += 1
            built += next_char
            if built == search_word:
                return next_point
        return None

    def dfs(self, start_p: Point, search_word: str) -> Union[Point, None]:
        for potential_positions in self.search_points:
            next_char, next_point = self.peek_next(start_p, potential_positions)
            if next_char == search_word[0]:
                found = self.non_rec_dfs(next_point, potential_positions, search_word, 0)
                if found:
                    return found
        return None


    def search(self, word: str) -> Union[Tuple[Point, Point], None]:
        start_from = word[0]
        rem = word[1:]
        for row, line in enumerate(self.puzzle):
            for idx, char in enumerate(line):
                if char == start_from:
                    p = Point(y=row, x=idx)
                    found = self.dfs(p, rem)
                    if found is not None:
                        return (p, found)


if __name__ == "__main__":
    puzzle = WordSearch(
        [
            "jefblpepre",
            "camdcimgtc",
            "oivokprjsm",
            "pbwasqroua",
            "rixilelhrs",
            "wolcqlirpc",
            "screeaumgr",
            "alxhpburyi",
            "jalaycalmp",
            "clojurermt",
        ]
    )
    print(puzzle.search("clojure"), (Point(0, 9), Point(6, 9)))
    print(puzzle.search("elixir"), (Point(5, 4), Point(0, 4)))
    print(puzzle.search("ecmascript"), (Point(9, 0), Point(9, 9)))
    print(puzzle.search("rust"), (Point(8, 4), Point(8, 1)))
    print(puzzle.search("java"), (Point(0, 0), Point(3, 3)))
    print(puzzle.search("lua"), (Point(7, 8), Point(5, 6)))
    print(puzzle.search("lisp"), (Point(2, 5), Point(5, 2)))
    print(puzzle.search("ruby"), (Point(7, 5), Point(4, 8)))
    print(puzzle.search("haskell"))
