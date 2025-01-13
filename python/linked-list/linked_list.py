from typing import Union


class Node:
    def __init__(self, value, previous=None):
        self.value = value
        self.previous = previous

    def __repr__(self):
        return f"{self.value}"


class LinkedList:
    def __init__(self):
        self.head: Union[Node, None] = None
        self.counter = 0

    def push(self, value: int) -> None:
        self.counter += 1
        as_node = Node(value=value)
        if self.head is None:
            self.head = as_node
        else:
            copied = self.head
            while copied.previous is not None:
                copied = copied.previous
            copied.previous = as_node

    def pop(self) -> Union[int, None]:
        if self.counter <= 0:
            raise IndexError("List is empty")

        self.counter = max(0, self.counter - 1)
        if self.head is None:
            return
        elif self.head.previous is None:
            copied = self.head
            self.head = None
            return copied.value
        copied = self.head
        lst = None
        while copied.previous:
            lst = copied
            copied = copied.previous

        lst.previous = None
        return copied.value

    def shift(self) -> int:
        if self.counter <= 0:
            raise IndexError("List is empty")

        copied = self.head
        self.counter = max(0, self.counter - 1)
        if copied.previous is None:
            self.head = None
            return copied.value

        self.head = copied.previous
        return copied.value

    def unshift(self, value: int) -> None:
        self.counter += 1
        new_head = Node(value=value)
        copied = self.head
        self.head = new_head
        new_head.previous = copied

    def delete(self, value: int) -> None:
        self.counter = max(0, self.counter - 1)
        if self.head == value:
            self.head = self.head.previous
        else:
            copied: Union[Node, None] = self.head
            changed = False
            last = copied
            while copied is not None:
                if copied.value == value:
                    last.previous = copied.previous
                    changed = True
                    break
                else:
                    last = copied
                    copied = copied.previous

            if not changed:
                raise ValueError("Value not found")

    def __repr__(self):
        copied = self.head
        incre = 1
        val = []
        while copied:
            val.append(f"Depth : {incre}, value : {copied}")
            incre += 1
            copied = copied.previous
        return "\n".join(val)

    def __len__(self):
        return self.counter


if __name__ == "__main__":
    lst = LinkedList()
    lst.push(97)
    lst.push(101)
    print(lst)
    lst.delete(101)
    print(len(lst), 1)
    print(lst.pop(), 97)
