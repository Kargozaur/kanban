import logging
from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, Protocol, cast


class UOWProvider(Protocol):
    uow: Any


P = ParamSpec("P")
R = ParamSpec("R")

logger = logging.getLogger(__name__)


def read_only[**P, R](
    func: Callable[P, Coroutine[Any, Any, R]] | Callable[P, Awaitable[R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    """Decorator for the services that are dependant on the unit of work.
    This decorator only executes get requests.
    """
    func_name = getattr(func, "__name__", "unknown_function")

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not args:
            raise IndexError("Decorator used on a function without the arguments")
        self_obj = cast(UOWProvider, args[0])
        if not hasattr(self_obj, "uow"):
            raise AttributeError(
                f"Unit of Work must to persist in {self_obj.__class__.__name__}"
            )
        async with self_obj.uow:
            try:
                return await func(*args, **kwargs)  # type: ignore
            except Exception as exc:
                logger.error(f"Transaction failed in {func_name}: {exc}")
                raise exc

    return wrapper
