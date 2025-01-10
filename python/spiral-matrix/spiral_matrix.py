from typing import List


class CreateSpiral:
    def __init__(self, size: int):
        self.size = size
        self.output = self.create()
        self.max_size = sum(len(mat) for mat in self.output)
        self.fill_output()

    def create(self) -> List[List[int]]:
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def fill_output(self) -> None:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        current_direction = 0
        row, col = 0, 0

        for num in range(1, self.max_size + 1):
            self.output[row][col] = num
            next_row = row + directions[current_direction][0]
            next_col = col + directions[current_direction][1]

            if (
                0 <= next_row < self.size
                and 0 <= next_col < self.size
                and self.output[next_row][next_col] == 0
            ):
                row, col = next_row, next_col
            else:
                current_direction = (current_direction + 1) % 4
                row += directions[current_direction][0]
                col += directions[current_direction][1]


def spiral_matrix(size: int) -> List[List[int]]:
    if size <= 0:
        return []

    spiral_space = CreateSpiral(size=size)
    return spiral_space.output


if __name__ == "__main__":
    spiral_matrix(5)
