import sys
import weakref
from src.main import weak_lru_cache
import gc


class SomeClass:
    @weak_lru_cache
    def weak_lru_cache_method(self, x: int) -> int:
        return x + 1

    @weak_lru_cache
    def weak_lru_cache_method2(self, x: int) -> int:
        return x + 1


def test_weak_lru_cache():
    obj = SomeClass()
    ref = weakref.ref(obj)
    for i in range(10):
        obj.weak_lru_cache_method(i)
        obj.weak_lru_cache_method2(i)
    assert weakref.getweakrefcount(obj) == 1
    assert sys.getrefcount(obj) == 2
    del obj
    gc.collect() == 0
    assert ref() is None
