from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging
import asyncio
from typing import Callable, Any, Coroutine

logger = logging.getLogger("antigravity")

def async_retry(
    max_attempts: int = 3,
    initial_wait: int = 1
):
    """
    Decorator for async functions to retry on exception with exponential backoff.
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=initial_wait, min=1, max=10),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )

def safe_execute(func: Callable, default_return: Any = None, *args, **kwargs):
    """
    Synchronous safe execution wrapper.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {e}", exc_info=True)
        return default_return

async def safe_execute_async(coro: Coroutine, default_return: Any = None):
    """
    Asynchronous safe execution wrapper.
    """
    try:
        return await coro
    except Exception as e:
        logger.error(f"Error in async execution: {e}", exc_info=True)
        return default_return
