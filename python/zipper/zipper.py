from typing import Dict, List, Any, Union
from enum import Enum


class Direction(Enum):
    left: str = "left"
    right: str = "right"
    ref: str = "ref"
    get_ref: str = "get_ref"


class Zipper:
    def __init__(self, tree) -> None:
        self.tree: Dict[str, Any] = tree
        self.search_depth = 0
        self.directions: List[Direction] = []

    @staticmethod
    def from_tree(tree: Dict):
        cls_instance = Zipper.__new__(Zipper)
        cls_instance.__init__(tree)
        return cls_instance

    def value(self):
        value = self._set_value_iter(Direction.get_ref)
        if value is None:
            return None
        return value["value"]

    def set_value(self, value: int):
        self._set_value_iter(Direction.ref, value)
        return self

    def left(self) -> Union["Zipper", None]:
        self.search_depth += 1
        self.directions.append(Direction.left)
        value: Union[Dict, None] = self._set_value_iter(Direction.get_ref)

        if value is None:
            return None
        return self

    def _set_value_iter(
        self,
        _direction: Direction,
        value: Union[int, None, dict] = None,
        _set_parent: bool = False,
    ) -> Union["Zipper", None]:
        ref = self.tree

        for depth, direction in enumerate(self.directions, start=1):
            if _set_parent and depth == self.search_depth:
                ref[direction.value] = value
                break

            ref = ref.get(direction.value)
            if ref is None:
                return ref

        if _direction == Direction.left or _direction == Direction.right:
            if type(value) is dict:
                ref[_direction.value] = value
            elif not _set_parent:
                ref[_direction.value]["value"] = value
        elif _direction == Direction.ref:
            ref["value"] = value
        return ref

    def set_left(self, value: int):
        self.search_depth += 1
        self.directions.append(Direction.left)
        self._set_value_iter(Direction.left, value, _set_parent=True)
        return self

    def right(self):
        self.search_depth += 1
        self.directions.append(Direction.right)
        value: Union[Dict, None] = self._set_value_iter(Direction.get_ref)
        if value is None:
            return None
        return self

    def set_right(self, value: Union[Dict, None]):
        self.search_depth += 1
        self.directions.append(Direction.right)
        self._set_value_iter(Direction.right, value, _set_parent=True)
        return self

    def up(self):
        if not self.directions:
            return None

        self.directions.pop()
        self.search_depth -= 1
        return self

    def to_tree(self):
        return self.tree

    def to_root(self):
        self.directions.clear()
