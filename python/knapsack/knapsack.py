from typing import List, Dict
from itertools import combinations

def gen_combos(items: List[Dict[str, int]]):
    n = len(items)
    for r in range(1, n + 1):
        for combo in combinations(range(n), r):
            yield list(dict.fromkeys(combo))

def maximum_value(maximum_value: int, items: Dict[str, int]) -> int:
    max_val = 0
    for combo in gen_combos(items):
        this_combo = [items[idx] for idx in combo]
        this_weight = sum((d["weight"] for d in this_combo))
        this_value = sum((d["value"] for d in this_combo))
        if this_weight <= maximum_value and this_value > max_val:
            max_val = this_value
    return max_val
