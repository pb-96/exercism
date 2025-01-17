from typing import List, TypedDict


class Item(TypedDict):
    weight: int
    value: int


def maximum_value(max_weight: int, items: List[Item]) -> int:
    dp_ar = [0 for _ in range(max_weight + 1)]
    for item in items:
        weight, value = item["weight"], item["value"]
        for w in reversed(range(weight, max_weight + 1)):
            dp_ar[w] = max(dp_ar[w], dp_ar[w - weight] + value)
    return dp_ar[max_weight]
