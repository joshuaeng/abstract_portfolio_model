import time
from typing import Callable
import logging


def inform(func: Callable):
    """Decorator method to give information on the execution of the decorated function."""
    def wrapper(**kwargs):
        """Wraps func"""
        start_time = time.time()
        logging.info(f"Execution {func.__name__}...")
        value = func(**kwargs)
        end_time = time.time()
        logging.info(f"{func.__name__} executed. Execution took {start_time - end_time} seconds.")
        return value
    return wrapper
