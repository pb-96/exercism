from typing import List

COMBINATIONS = {
    2: "abc",
    3: "def",
    4: "ghi",
    5: "jkl",
    6: "mno",
    7: "pqrs",
    8: "tuv",
    9: "wxyz",
}


def generate_combinations(numbers: List[int]) -> List[str]:
    combinations = [char for char in COMBINATIONS.get(numbers.pop())]
    for number in numbers:
        next_combinations = COMBINATIONS.get(number)
        new_combinations = []
        for char in next_combinations:
            for to_combine in combinations:
                new_combinations.append(char + to_combine)
        combinations = new_combinations
    return combinations


def get_potential_messages(numbers_typed: str):
    if not numbers_typed:
        return []
    numbers = [*map(int, numbers_typed)]
    return generate_combinations(numbers)
