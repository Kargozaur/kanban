from functools import wraps

import logging

logger = logging.getLogger(__name__)


def transactional(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not hasattr(self, "uow"):
            raise AttributeError(
                f"{self.__class__.__name__} must have a 'uow' attribute"
            )
        async with self.uow:
            try:
                result = await func(self, *args, **kwargs)
                logger.info(f"DEBUG - result = {result}")
                await self.uow.commit()
                return result
            except Exception as exc:
                await self.uow.rollback()
                logger.error(
                    f"Transaction failed in {func.__name__}: {exc}"
                )
                raise exc

    return wrapper
