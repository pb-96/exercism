from typing import List, Dict, Any


def tree_from_traversals(pre_order: List[str], in_order: List[str]) -> Dict[str, Any]:
    if len(pre_order) != len(in_order):
        raise ValueError("traversals must have the same length")

    elif set(pre_order) != set(in_order):
        raise ValueError("traversals must have the same elements")

    elif len(set(pre_order)) != len(pre_order) or len(set(in_order)) != len(in_order):
        raise ValueError("traversals must contain unique items")

    elif len(pre_order) == 0:
        return {}

    value = pre_order[0]
    adjacent_index = in_order.index(value)

    return {
        "v": value,
        "l": tree_from_traversals(
            pre_order=pre_order[1 : 1 + adjacent_index],
            in_order=in_order[:adjacent_index],
        ),
        "r": tree_from_traversals(
            pre_order=pre_order[adjacent_index + 1: ],
            in_order=in_order[adjacent_index + 1: ]
        )
    }


if __name__ == "__main__":
    pre_order = ["a", "i", "x", "f", "r"]
    in_order = ["i", "a", "f", "x", "r"]
    print(tree_from_traversals(pre_order, in_order))
