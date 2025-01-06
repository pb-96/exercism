from typing import Union, List, Generator, Iterable


class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.data_as_int = int(data)

    def __str__(self):
        return f"TreeNode(data={self.data}, left={self.left}, right={self.right})"


TreeNodeOrNone = Union[TreeNode, None]


class BinarySearchTree:
    def __init__(self, tree_data: List[str]) -> None:
        self.tree_data = tree_data
        self.head = TreeNode(self.tree_data[0], None, None)
        for node in self.tree_data[1:]:
            self.insert_node(self.head, TreeNode(node))

    def insert_node(self, curr: TreeNode, to_add: TreeNode) -> None:
        if to_add.data_as_int > curr.data_as_int:
            if curr.right is None:
                curr.right = to_add
            else:
                self.insert_node(curr.right, to_add)
        else:
            if curr.left is None:
                curr.left = to_add
            else:
                self.insert_node(curr.left, to_add)

    def __iter__(self) -> Iterable[str]:
        return iter((n.data for n in self.search_tree(self.head)))

    def data(self) -> "TreeNode":
        return self.head

    def sorted_data(self) -> List[int]:
        return list(self)

    def search_tree(self, start_node: TreeNodeOrNone) -> Generator["TreeNode"]:
        if start_node is not None:
            yield from self.search_tree(start_node.left)
            yield start_node
            yield from self.search_tree(start_node.right)

    def compare_trees(self, tree_one: TreeNodeOrNone, tree_two: TreeNodeOrNone) -> bool:
        if not tree_one and not tree_two:
            return True
        if tree_one and tree_two:
            return (
                tree_one.data == tree_two.data
                and self.compare_trees(tree_one.left, tree_two.left)
                and self.compare_trees(tree_one.right, tree_two.right)
            )
        return False
