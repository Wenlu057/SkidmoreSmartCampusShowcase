class MinHeap:
    def __init__(self):
        self._a = []
    def __len__(self): return len(self._a)
    def push(self, x):
        self._a.append(x)
        self._sift_up(len(self._a)-1)
    def pop(self):
        if not self._a: raise IndexError("pop from empty")
        self._a[0], self._a[-1] = self._a[-1], self._a[0]
        x = self._a.pop()
        if self._a: self._sift_down(0)
        return x
    def peek(self):
        if not self._a: raise IndexError("peek from empty")
        return self._a[0]
    def _sift_up(self, i):
        while i:
            p = (i-1)//2
            if self._a[p] <= self._a[i]: break
            self._a[p], self._a[i] = self._a[i], self._a[p]
            i = p
    def _sift_down(self, i):
        n = len(self._a)
        while True:
            l = 2*i+1; r = l+1; s = i
            if l < n and self._a[l] < self._a[s]: s = l
            if r < n and self._a[r] < self._a[s]: s = r
            if s == i: break
            self._a[i], self._a[s] = self._a[s], self._a[i]
            i = s
