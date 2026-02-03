import logging
from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any, ParamSpec, Protocol, cast


class UOWProvider(Protocol):
    uow: Any


P = ParamSpec("P")
R = ParamSpec("R")

logger = logging.getLogger(__name__)


def transactional[**P, R](
    func: Callable[P, Coroutine[Any, Any, R]] | Callable[P, Awaitable[R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    """Decorator for the services that are dependant on the unit of work.
    Should be used only on the methods, that are requiring commits or rollbacks.
    """
    func_name = getattr(func, "__name__", "unknown_function")

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        if not args:
            raise IndexError("Decorator used on a function without the arguments")
        self_obj = cast(UOWProvider, args[0])
        if not hasattr(self_obj, "uow"):
            raise AttributeError(
                f"{self_obj.__class__.__name__} must have a 'uow' attribute"
            )
        async with self_obj.uow:
            try:
                result = await func(*args, **kwargs)  # type: ignore
                await self_obj.uow.commit()
                return result
            except Exception as exc:
                await self_obj.uow.rollback()
                logger.error(f"Transaction failed in {func_name}: {exc}")
                raise exc

    return wrapper
