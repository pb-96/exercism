from typing import List

def apply_encoding(message, rails):
    encoded = []
    for _ in range(rails):
        encoded.append(["" for _ in range(len(message))])

    pointer = (0, 0)
    down = True

    for chars in message:
        row, col = pointer
        encoded[row][col] = chars

        if row >= len(encoded) - 1:
            down = False
        elif row == 0:
            down = True

        if down:
            row += 1
        else:
            row -= 1

        pointer = (row, col + 1)
    return encoded

def encode(message: str, rails: int):
    encoded = apply_encoding(message, rails)
    encoded_msg = ""
    for row in encoded:
        encoded_msg += "".join(row)
    return encoded_msg


def calculate_chars_per_rail(message_length, rails):
    chars_per_rail = [0] * rails
    rail = 0
    down = True

    for _ in range(message_length):
        chars_per_rail[rail] += 1
        if rail == 0:
            down = True
        elif rail == rails - 1:
            down = False

        rail += 1 if down else -1

    return chars_per_rail


def decode(encoded_message, rails):
    chars_per_line = calculate_chars_per_rail(len(encoded_message), rails)
    chunked_message: List[List[str]] = []
    start = 0
    for index in chars_per_line:
        given_line = list(encoded_message[start: start + index])
        chunked_message.append(given_line)
        start += index

    start = 0
    down = True
    original_message = []

    while True:
        to_pop = chunked_message[start]
        if not to_pop:
            break

        next_char = to_pop.pop(0)
        original_message.append(next_char)

        if start == len(chunked_message) - 1:
            down = False
        elif start == 0:
            down = True
        
        if down:
            start += 1
        else:
            start -=1 
        
    return "".join(original_message)

