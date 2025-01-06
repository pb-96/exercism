from typing import List
import operator


class StackUnderflowError(Exception):
    pass


OPERATOR_STACK = {
    "-": operator.sub,
    "+": operator.add,
    "/": operator.floordiv,
    "*": operator.mul,
}

KEY_WORDS = {
    "dup",
    "drop",
    "swap",
    "over",
}
MINIMUM_STACK = 2


class NumericList(list):
    def add(self, object):
        as_int = int(object)
        return super().append(as_int)


class Matcher:
    def __init__(self):
        # self.input_data: List[str] = input_data
        self.rolling_stack = NumericList()
        self.declaring_var = False
        self.cached_vars = {}

    def raise_less_than(self):
        if len(self.rolling_stack) < MINIMUM_STACK:
            raise StackUnderflowError("Insufficient number of items in stack")

    def raise_empty(self):
        if not self.rolling_stack:
            raise StackUnderflowError("Insufficient number of items in stack")

    def raise_on_input(self, input_data):
        if len(input_data) == 1:
            raise ValueError("illegal operation")

    def match(self, input_data):
        for commands in input_data:
            if commands.startswith(":") and commands.endswith(";"):
                self.raise_on_input(input_data)
                self.process_vars(commands)
            else:
                self.process_cmd(commands)

    def process_cmd(self, commands: str):
        for char in commands.split():
            lowered = char.lower()
            if lowered in self.cached_vars:
                self.match(self.cached_vars[lowered])
            elif char.isnumeric() or char.replace("-", "").isnumeric():
                self.rolling_stack.add(char)
            elif char in OPERATOR_STACK:
                self.process_operator(char)
            elif lowered in KEY_WORDS:
                self.process_lowered(lowered)
            else:
                raise ValueError("undefined operation")

    def process_lowered(self, lowered: str):
        match (lowered):
            case "dup":
                self.raise_empty()
                self.rolling_stack.add(self.rolling_stack[-1])
            case "drop":
                self.raise_empty()
                self.rolling_stack.pop()
            case "swap":
                self.raise_less_than()
                last = self.rolling_stack.pop(-2)
                self.rolling_stack.add(last)
            case "over":
                self.raise_less_than()
                copy = self.rolling_stack[-2]
                self.rolling_stack.add(copy)

    def process_operator(self, char: str):
        self.raise_less_than()
        to_apply = OPERATOR_STACK.get(char)
        elem = self.rolling_stack[-2:]
        if elem[-1] == 0 and char == "/":
            raise ZeroDivisionError("divide by zero")

        self.rolling_stack = NumericList(self.rolling_stack[:-2])
        to_append = to_apply(*elem)
        self.rolling_stack.add(to_append)

    def process_vars(self, commands: str):
        commands = commands[1:-1].strip().split()
        commands_iter = iter(commands)
        var_name = next(commands_iter).lower()
        updated_commands = []
        for char in commands_iter:
            if char in self.cached_vars:
                updated_commands.extend(self.cached_vars[char])
            else:
                updated_commands.append(char.lower())
        self.cached_vars[var_name] = updated_commands


def evaluate(input_data: List[str]):
    matcher: Matcher = Matcher()
    matcher.match(input_data)
    return matcher.rolling_stack
