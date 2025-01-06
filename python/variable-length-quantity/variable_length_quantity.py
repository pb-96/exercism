from typing import List

UPPER_LIM = 0x7F


def encode(numbers: List[bytes]) -> List[bytes]:
    ret = []
    for number in numbers:
        collect = [number & 0x7F]
        number >>= 7
        while number:
            collect.append(0x80 + (number & 0x7F))
            number >>= 7
        ret += collect[::-1]
    return ret

def decode(bytes_):
    numbers = []
    collect = 0
    byte = None
    for byte in bytes_:
        if byte & 0x80:
            collect += byte & 0x7F
            collect <<= 7
        else:
            collect += byte
            numbers.append(collect)
            collect = 0
    if byte & 0x80:
        raise ValueError("incomplete sequence")
    return numbers

