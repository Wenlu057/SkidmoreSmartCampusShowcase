from __future__ import annotations
from typing import Optional, Tuple, List

_DELETED = object()

class HashMap:
    def __init__(self, capacity: int = 8):
        self._n = 0
        self._cap = capacity
        self._a: List[Optional[Tuple[object, object]]] = [None] * self._cap

    def _idx(self, key):
        return (hash(key) & 0x7fffffff) % self._cap

    def _rehash(self, newcap):
        old = [x for x in self._a if x and x is not _DELETED]
        self._cap = newcap
        self._a = [None] * self._cap
        self._n = 0
        for k, v in old:
            self.put(k, v)

    def _load(self):
        return self._n / self._cap

    def put(self, key, value) -> None:
        if self._load() > 0.6:
            self._rehash(self._cap * 2)
        i = self._idx(key)
        first_del = None
        while True:
            slot = self._a[i]
            if slot is None:
                if first_del is None:
                    self._a[i] = (key, value)
                else:
                    self._a[first_del] = (key, value)
                self._n += 1
                return
            if slot is _DELETED:
                if first_del is None: first_del = i
            else:
                k, _ = slot
                if k == key:
                    self._a[i] = (key, value)
                    return
            i = (i + 1) % self._cap

    def get(self, key):
        i = self._idx(key)
        while True:
            slot = self._a[i]
            if slot is None:
                return None
            if slot is not _DELETED:
                k, v = slot
                if k == key:
                    return v
            i = (i + 1) % self._cap

    def remove(self, key):
        i = self._idx(key)
        while True:
            slot = self._a[i]
            if slot is None:
                return None
            if slot is not _DELETED:
                k, v = slot
                if k == key:
                    self._a[i] = _DELETED
                    self._n -= 1
                    return v
            i = (i + 1) % self._cap

    def __contains__(self, key):
        return self.get(key) is not None
