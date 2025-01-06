from typing import List
import operator
from collections import deque
from functools import partial

OPERATOR_STACK = {
    "-": operator.sub,
    "+": operator.add,
    "/": operator.floordiv,
    "*": operator.mul,
}

global_cache = set()


class InputCell:
    def __init__(self, initial_value):
        self.value = initial_value
        self.mem_id = id(self)
        self.operand_stack = deque([])
        self.callbacks = []

    def __add__(self, other):
        if isinstance(other, InputCell):
            return self.value + other.value
        elif isinstance(other, (int, float)):
            return self.value + other

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, InputCell):
            return self.value * other.value
        elif isinstance(other, (int, float)):
            return self.value * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __setattr__(self, name, value):
        if name == "value":
            if hasattr(self, name):
                global_cache.add(id(self))
            if hasattr(self, "callbacks"):
                for callback in self.callbacks:
                    callback(value)
        super().__setattr__(name, value)


class ComputeCell:
    def __init__(self, inputs: List[InputCell], compute_functions):
        self.value = compute_functions(inputs)
        self.inputs = inputs
        self.compute_functions = compute_functions
        self.mem_cache = {id(sources) for sources in inputs}
        self.callbacks = []

    def add_callback(self, callback):
        for child in self.inputs:
            child.callbacks.append(callback)

        self.callbacks.append(callback)

    def remove_callback(self, callback):
        # self.compute_function
        ...

    def __getattr__(self, attr):
        return super().__getattr__(self, attr)

    def __getattribute__(self, attr):
        if attr == "value":
            new_value = self.compute_functions(self.inputs)
            setattr(self, attr, new_value)
            if self.callbacks:
                for child in self.inputs:
                    for cb in child.callbacks:
                        cb(new_value)
            return super().__getattribute__(attr)
        return super().__getattribute__(attr)

    def __add__(self, other):
        if isinstance(other, (InputCell, ComputeCell)):
            return self.value + other.value
        elif isinstance(other, (int, float)):
            return self.value + other

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (InputCell, ComputeCell)):
            return self.value * other.value
        elif isinstance(other, (int, float)):
            return self.value * other


if __name__ == "__main__":

    def callback_factory(observer):
        def callback(observer, value):
            observer.append(value)

        return partial(callback, observer)

    input = InputCell(1)
    output = ComputeCell(
        [
            input,
        ],
        lambda inputs: inputs[0] + 1,
    )

    cb1_observer = []
    callback1 = callback_factory(cb1_observer)
    output.add_callback(callback1)
    print(cb1_observer, "Here")
    input.value = 3
    print(input.value)
    print(cb1_observer)
