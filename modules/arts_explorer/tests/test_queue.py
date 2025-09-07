from ..ds.queue import Queue

def test_fifo():
    q = Queue()
    for i in range(5): q.enqueue(i)
    out = [q.dequeue() for _ in range(5)]
    assert out == list(range(5))
