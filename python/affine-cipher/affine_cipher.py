from math import gcd, pow
from functools import partial


def is_co_prime(fn):
    def inner(*args):
        _, a, _ = args
        if gcd(a, 26) > 1:
            raise ValueError("a and m must be coprime.")
        return fn(*args)

    return inner


@is_co_prime
def encode(plain_text: str, a: int, b: int) -> str:
    plain_text = plain_text.lower()
    partial_cipher = partial(apply_cipher, a=a, b=b)
    ciphered_chars = "".join(
        (partial_cipher(char=char) for char in plain_text if char.isalnum())
    )
    return slide_window(ciphered_chars)


@is_co_prime
def decode(ciphered_text: str, a: int, b: int) -> str:
    decipher_func = partial(apply_decipher, a=a, b=b)
    joined = "".join(
        (decipher_func(char=char) for char in ciphered_text if char != " ")
    )
    return joined


def apply_decipher(a: int, b: int, char: str, m=26) -> str:
    if char.isdigit():
        return char

    for rotated in range(0, m):
        if (a * rotated) % m == 1:
            break

    y = ord(char) - 97
    return chr(rotated * (y - b) % m + 97)


def apply_cipher(a: int, b: int, char: str, m=26) -> str:
    if char.isdigit():
        return char

    x = ord(char) - 97
    rel = (a * x + b) % m + 97
    return chr(rel)


def slide_window(strs: str, window: int = 5) -> str:
    if len(strs) <= window:
        return strs

    windows = []
    pointer = 0
    for _ in range((len(strs) // window) + 1):
        to = min(len(strs), pointer + window)
        windows.append(strs[pointer:to])
        pointer = to

    return " ".join(windows).strip()
