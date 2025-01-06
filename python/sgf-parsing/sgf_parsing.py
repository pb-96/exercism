from enum import Enum
from typing import Set, Tuple


class SgfTree:
    def __init__(self, properties=None, children=None):
        self.properties = properties or {}
        self.children = children or []

    def __eq__(self, other):
        if not isinstance(other, SgfTree):
            return False
        for key, value in self.properties.items():
            if key not in other.properties:
                return False
            if other.properties[key] != value:
                return False
        for key in other.properties.keys():
            if key not in self.properties:
                return False
        if len(self.children) != len(other.children):
            return False
        for child, other_child in zip(self.children, other.children):
            if child != other_child:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __repr__(self) -> str:
        return f"SgfTree(properties={self.properties}, children={self.children})"


class TargetSequence(Enum):
    COLON = ";"
    OPENING = "("
    CLOSING = ")"
    CHILDREN_START = "["
    CHILDREN_END = "]"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


def char_accepted(strs: str) -> bool:
    return strs.isalpha() or strs.isspace() or strs in ["\\", "\n", "(", ")", "="]


def recursive_parse(
    input_str: str, node: SgfTree, is_recursive: bool = False
) -> Tuple[SgfTree, Set[int]]:
    node_key = ""
    start_found, is_in_child_section = False, False
    buffer = ""
    last_key = None
    index = 0
    copied = input_str
    data = []

    while index < len(copied):
        current_char = copied[index]

        if current_char in ["\t"]:
            current_char = " "
        elif current_char == "\\":
            check_next = copied[index + 1]
            if check_next == "\\":
                index += 1
            elif check_next in ["[", "]"] or check_next.isalpha():
                current_char = check_next
                index += 1
            elif check_next == "\t":
                current_char = " "
                index += 1
            elif check_next == "\n":
                current_char = ""
                index += 1
            process_as_string = True
        else:
            process_as_string = char_accepted(current_char) or (
                is_in_child_section and current_char in ["[", ";"]
            )

        if not process_as_string:
            if current_char == TargetSequence.COLON.value:
                if start_found and not is_in_child_section:
                    new_index, child_node = recursive_parse(
                        input_str[index:], SgfTree(), True
                    )
                    node.children.append(child_node)
                    index += new_index
                    continue
                else:
                    start_found = True

            elif current_char == TargetSequence.CHILDREN_START.value:
                # collect all string values into array here
                is_in_child_section = True

            elif current_char == TargetSequence.CHILDREN_END.value:
                if node_key or last_key:
                    if buffer != "":
                        data.append(buffer)
                        buffer = ""

                    if not data:
                        index += 1
                        continue

                    data = ["".join(data)]
                    if node_key:
                        properties = {node_key: data}
                        node.properties.update(properties)
                    else:
                        node.properties[last_key].extend(data)

                    if is_recursive:
                        return index, node
                    if node_key:
                        last_key = node_key

                    is_in_child_section = False
                    node_key = None
                    data = []

        elif process_as_string:
            if not is_in_child_section:
                if current_char.islower() and not is_recursive:
                    raise ValueError("property must be in uppercase")
                elif node_key is None:
                    node_key = current_char
                else:
                    node_key += current_char
            elif current_char.isspace():
                if buffer:
                    data.append(buffer)

                data.append(current_char)
                buffer = ""
            else:
                buffer += current_char
        index += 1

    return index, node


def parse(input_string: str) -> str:
    if input_string.isspace() or input_string in [";", ""]:
        raise ValueError("tree missing")
    if input_string == "()":
        raise ValueError("tree with no nodes")
    if input_string == "(;)":
        return SgfTree()
    if input_string.find("[") < 0:
        raise ValueError("properties without delimiter")

    node = SgfTree()
    removed_first_and_last = input_string[1:-1]
    recursive_parse(removed_first_and_last, node)
    return node
