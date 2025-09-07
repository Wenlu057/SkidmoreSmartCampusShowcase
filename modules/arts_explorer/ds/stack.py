class Stack:
    def __init__(self):
        self._data = []
    def push(self, x):
        self._data.append(x)
    def pop(self):
        if not self._data: raise IndexError("pop from empty")
        return self._data.pop()
    def peek(self):
        if not self._data: raise IndexError("peek from empty")
        return self._data[-1]
    def is_empty(self):
        return not self._data
