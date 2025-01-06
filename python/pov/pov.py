from json import dumps
from typing import List, cast, Union, Dict
from collections import OrderedDict


class Tree:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []
        self.src_path = OrderedDict({self.label: self.children})

    def __repr__(self):
        if self.children:
            return f"Tree({self.label}, children={self.children})"
        return f"Tree({self.label})"

    def __dict__(self):
        return {self.label: [c.__dict__() for c in sorted(self.children)]}

    def __str__(self, indent=None):
        return dumps(self.__dict__(), indent=indent)

    def __lt__(self, other):
        return self.label < other.label

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()

    def reorient(self, path_to_result: Dict[str, "Tree"], from_node: str):
        return_cls = path_to_result.pop(from_node)
        keys = [*path_to_result.keys()]
        iter_node = return_cls

        while keys:
            src_node = keys.pop()
            to_severe: "Tree" = path_to_result[src_node]
            severed = []
            child: "Tree"
            for child in to_severe.children:
                if child.label == iter_node.label:
                    continue
                severed.append(child)
            to_severe.children = severed
            iter_node.children.append(to_severe)
            iter_node = to_severe
        return return_cls, iter_node

    def from_pov(self, from_node: str) -> "Tree":
        if from_node == self.label:
            return self

        path_to_result = self.dfs(self, from_node, self.src_path)
        if path_to_result is None:
            raise ValueError("Tree could not be reoriented")

        root: List["Tree"] = path_to_result.pop(self.label)
        root_children = []

        for child in root:
            if child.label in path_to_result:
                continue
            root_children.append(child)

        updated_root = Tree(self.label, root_children)
        to_return, to_append = self.reorient(
            path_to_result=path_to_result, from_node=from_node
        )
        to_append.children.append(updated_root)
        return to_return

    def dfs(
        self,
        start_node: "Tree",
        target_node: str,
        path: OrderedDict[str, "Tree"] = None,
    ) -> Union[Dict[str, "Tree"], None]:
        if start_node.label == target_node:
            return path

        if path is None:
            return

        for child in start_node.children:
            child = cast(Tree, child)
            path[child.label] = child

            if child.label == target_node:
                return path

            if not child.children:
                path.pop(child.label)
                continue

            full_path = self.dfs(child, target_node=target_node, path=path)
            if full_path is not None:
                return full_path
            else:
                path.pop(child.label)

    def path_to(self, from_node: str, to_node: str) -> "Tree":
        root = self.dfs(self, from_node, OrderedDict(**self.src_path))
        if root is None:
            raise ValueError("Tree could not be reoriented")

        copy = self.__class__(self.label, self.children)
        adjacent_path = self.dfs(copy, to_node, OrderedDict(**copy.src_path))
        if adjacent_path is None:
            raise ValueError("No path found")

        common_keys = OrderedDict()
        for k in root:
            if adjacent_path.get(k) is not None:
                common_keys[k] = True

        common_keys = list(common_keys.keys())
        first_ancestor = common_keys[-1]
        root_keys = list(root.keys())
        root_keys = root_keys[root_keys.index(first_ancestor) :][::-1]
        adjacent_path_keys = list(adjacent_path.keys())
        adjacent_path_keys = adjacent_path_keys[
            adjacent_path_keys.index(first_ancestor) + 1 :
        ]
        return root_keys + adjacent_path_keys
