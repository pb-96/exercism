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


def validate(string):
    if len(string) < 2:
        raise ValueError("tree missing")
    if string[1] != ";":
        raise ValueError("tree with no nodes")
    if string[0] != "(" or string[-1] != ")" or string[1] != ";":
        raise ValueError("string format (; ... ) expected")


def parse(string):
    validate(string)
    return preparse(string[2:-1])


def read_subtree(string):
    escaping = False
    read_val = False
    level = 0
    subtree = ""

    for char in string:
        subtree += char
        if read_val:
            if escaping:
                escaping = False
                continue
            if char == "\\":
                escaping = True
                continue
            if char == "]":
                read_val = False
                continue
            continue
        if char == "[":
            read_val = True
            continue
        if char == "(":
            level += 1
            continue
        if char == ")":
            level -= 1
            if level == 0:
                break
    return subtree


def preparse(string):
    skipping = 0
    read_prop = True
    read_val = False
    escaping = False

    new_prop = ""
    old_prop = ""

    properties = {}
    children = []

    for idx in range(len(string)):
        if skipping:
            skipping -= 1
            continue

        char = string[idx]

        if read_prop:
            if char.isupper():
                new_prop += char
                read_val = False  # consider "(;A[a]B;)"
                continue
            if char == "[":
                if not new_prop:
                    if not old_prop:
                        raise ValueError("value without property")
                    new_prop = old_prop
                new_val = ""
                read_prop = False
                read_val = True
                continue
            if read_val:
                if char == ";":
                    children.append(preparse(string[idx + 1 :]))
                    break
                if char == "(":
                    sub = read_subtree(string[idx:])
                    children.append(parse(sub))
                    skipping = len(sub) - 1
                    continue
            raise ValueError("property must be in uppercase")

        if read_val:
            if char == "\t":
                char = " "
            if escaping:
                if char != "\n":
                    new_val += char
                escaping = False
                continue
            if char == "\\":
                escaping = True
                continue
            if char == "]":
                if new_prop == old_prop:
                    properties[old_prop].append(new_val)
                else:
                    old_prop = new_prop
                    properties[new_prop] = [new_val]
                read_prop = True
                new_prop = ""
                continue
            new_val += char
            continue

    if new_prop:
        raise ValueError("properties without delimiter")

    return SgfTree(properties, children)
