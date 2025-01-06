from typing import List

UPPER_LIM = 0x7F


def encode(numbers: List[bytes]) -> List[bytes]:
    results = []
    for number in numbers:
        result = 0
        result = (result << number) | (number & UPPER_LIM)
        results.append(result)

    return results


def decode(bytes_):
    pass


if __name__ == "__main__":
    print(encode([0x2000]))
