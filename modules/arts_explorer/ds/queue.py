class Queue:
    def __init__(self):
        self._data = []
        self._head = 0
    def enqueue(self, x):
        self._data.append(x)
    def dequeue(self):
        if self.is_empty(): raise IndexError("dequeue from empty")
        x = self._data[self._head]
        self._head += 1
        if self._head > 32 and self._head * 2 > len(self._data):
            self._data = self._data[self._head:]; self._head = 0
        return x
    def is_empty(self):
        return self._head >= len(self._data)
