from __future__ import annotations
from typing import List, Callable, Any

def selection_sort(a: List, key=lambda x: x, reverse=False):
    arr = a[:]
    n = len(arr)
    for i in range(n):
        m = i
        for j in range(i+1, n):
            if reverse:
                if key(arr[j]) > key(arr[m]): m = j
            else:
                if key(arr[j]) < key(arr[m]): m = j
        arr[i], arr[m] = arr[m], arr[i]
    return arr

def insertion_sort(a: List, key=lambda x: x, reverse=False):
    arr = a[:]
    for i in range(1, len(arr)):
        x = arr[i]
        j = i-1
        while j >= 0 and ((key(arr[j]) > key(x) and not reverse) or (key(arr[j]) < key(x) and reverse)):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = x
    return arr

def merge_sort(a: List, key=lambda x: x, reverse=False):
    arr = a[:]
    if len(arr) <= 1: return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid], key, reverse)
    right = merge_sort(arr[mid:], key, reverse)
    return _merge(left, right, key, reverse)

def _merge(left, right, key, reverse):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        lv, rv = key(left[i]), key(right[j])
        if (lv <= rv and not reverse) or (lv >= rv and reverse):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out
