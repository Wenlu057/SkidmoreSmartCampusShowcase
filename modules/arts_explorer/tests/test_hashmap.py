from ..ds.hashmap import HashMap

def test_basic_put_get():
    m = HashMap()
    m.put("a", 1)
    m.put("b", 2)
    assert m.get("a") == 1
    assert m.get("b") == 2

def test_overwrite_and_remove():
    m = HashMap()
    m.put("x", 1)
    m.put("x", 3)
    assert m.get("x") == 3
    assert m.remove("x") == 3
    assert m.get("x") is None
