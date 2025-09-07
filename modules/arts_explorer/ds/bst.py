from __future__ import annotations
from typing import Optional, Iterator, Tuple

class _N:
    __slots__ = ("k","v","l","r")
    def __init__(self, k, v):
        self.k, self.v, self.l, self.r = k, v, None, None

class BST:
    def __init__(self):
        self._root: Optional[_N] = None

    def insert(self, k, v):
        def _ins(n, k, v):
            if n is None: return _N(k, v)
            if k < n.k: n.l = _ins(n.l, k, v)
            elif k > n.k: n.r = _ins(n.r, k, v)
            else: n.v = v
            return n
        self._root = _ins(self._root, k, v)

    def find(self, k):
        n = self._root
        while n:
            if k < n.k: n = n.l
            elif k > n.k: n = n.r
            else: return n.v
        return None

    def inorder(self) -> Iterator[Tuple[object, object]]:
        def _in(n):
            if not n: return
            yield from _in(n.l)
            yield (n.k, n.v)
            yield from _in(n.r)
        return iter(list(_in(self._root)))
