class InputCell:
    def __init__(self, initial_value):
        self._value = initial_value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for c in self._callbacks:
            c(value)

    def add_callback(self, callback):
        self._callbacks.append(callback)


class ComputeCell:
    def __init__(self, inputs, compute_function):
        self._compute_function = compute_function
        self._inputs = inputs
        self._callbacks = []
        self._current_value = None
        self.changed(None)
        for i in inputs:
            i.add_callback(self.changed)

    @property
    def value(self):
        return self._compute_function([i.value for i in self._inputs])

    def changed(self, _):
        if self.value != self._current_value:
            self._current_value = self.value
            for c in self._callbacks:
                c(self.value)

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def remove_callback(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)
