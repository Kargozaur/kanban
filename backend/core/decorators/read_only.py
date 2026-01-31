from functools import wraps

import logging

logger = logging.getLogger(__name__)


def read_only(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not hasattr(self, "uow"):
            raise AttributeError(
                f"Unit of Work must to persist in {self.__class__.__name__}"
            )
        async with self.uow:
            try:
                result = await func(self, *args, **kwargs)
                return result
            except Exception as exc:
                logger.error(
                    f"Transaction failed in {func.__name__}: {exc}"
                )
                raise exc

    return wrapper
