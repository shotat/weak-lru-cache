from typing import Callable, ParamSpec, TypeVar, Concatenate, Any

from functools import lru_cache, wraps
import weakref

P = ParamSpec("P")
R_co = TypeVar("R_co")


def weak_lru_cache(
    func: Callable[Concatenate[Any, P], R_co],
    maxsize: int = 128,
) -> Callable[Concatenate[Any, P], R_co]:
    """lru_cache with weak references"""

    @lru_cache(maxsize=maxsize)
    def _cached_func(
        self_ref: weakref.ReferenceType,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R_co:
        self = self_ref()
        if self is None:
            raise ReferenceError("The object has been garbage collected")
        return func(self, *args, **kwargs)

    @wraps(func)
    def wrapper(
        self: Any,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R_co:
        return _cached_func(weakref.ref(self), *args, **kwargs)  # type: ignore[arg-type]

    return wrapper
