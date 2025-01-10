from typing import List, Dict
from itertools import chain, combinations


def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss) + 1)))


def maximum_value(maximum_weight: int, items: List[Dict[str, int]]):
    if not items or len(items) <= 1:
        return 0

    subsets = all_subsets(items)
    max_value = 0

    for row in subsets:
        curr_weight, curr_val = 0, 0
        d: Dict
        for d in row:
            weight, value = d.get("weight"), d.get("value")
            curr_weight += weight
            curr_val += value

        if curr_weight > maximum_weight:
            continue

        if curr_val > max_value:
            max_value = curr_val

    return max_value


if __name__ == "__main__":
    items = [
        {"weight": 2, "value": 5},
        {"weight": 2, "value": 5},
        {"weight": 2, "value": 5},
        {"weight": 2, "value": 5},
        {"weight": 10, "value": 21},
    ]
    print(maximum_value(10, items))