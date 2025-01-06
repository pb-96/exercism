NODE, EDGE, ATTR = range(3)


class Node:
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs

    def __eq__(self, other):
        return self.name == other.name and self.attrs == other.attrs

    def __repr__(self):
        return f"name:{self.name} properties:{self.attrs}"


class Edge:
    def __init__(self, src, dst, attrs):
        self.src = src
        self.dst = dst
        self.attrs = attrs

    def __eq__(self, other):
        return (
            self.src == other.src
            and self.dst == other.dst
            and self.attrs == other.attrs
        )

    def __repr__(self) -> str:
        return f"self.src={self.src},self.dst={self.dst}, self.attrs={self.attrs}"


class Graph:
    def __init__(self, data=None):
        self.edges = []
        self.nodes = []
        self.attrs = {}
        self.data = data or []

        if not isinstance(self.data, (tuple, set, list)):
            raise TypeError("Graph data malformed")

        for T in self.data or []:
            if not len(T) > 1:
                raise TypeError("Graph item incomplete")

            data_type, *args = T
            match data_type:
                case 0:
                    if not len(args) == 2:
                        raise ValueError("Node is malformed")

                    node = Node(*args)
                    self.nodes.append(node)

                case 1:
                    if not len(args) == 3:
                        raise ValueError("Edge is malformed")

                    edge = Edge(*args)
                    self.edges.append(edge)

                case 2:
                    if not len(args) == 2:
                        raise ValueError("Attribute is malformed")

                    key, value = args
                    self.attrs[key] = value
                case _:
                    raise ValueError("Unknown item")


if __name__ == "__main__":
    Graph(1)
