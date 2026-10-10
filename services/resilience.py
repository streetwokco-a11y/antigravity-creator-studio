"""
services/resilience.py - Fault tolerance & Dead-Letter Queue decorators.
"""

import time
import functools
import traceback
from typing import Callable, Any
from services.db_service import record_dead_letter


def resilient_job(service_name: str, max_retries: int = 3, initial_delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"[{service_name}] Attempt {attempt}/{max_retries} failed: {e}")
                    if attempt < max_retries:
                        time.sleep(delay)
                        delay *= 2.0

            # Permanent failure handler: Store trace in SQLite dead-letter queue
            error_msg = f"{str(last_exception)}\n{traceback.format_exc()}"
            payload = {"args": [str(a) for a in args], "kwargs": {k: str(v) for k, v in kwargs.items()}}
            record_dead_letter(service_name, payload, error_msg, max_retries)
            raise RuntimeError(f"Job {service_name}.{func.__name__} failed permanently after {max_retries} retries: {last_exception}")
        return wrapper
    return decorator
