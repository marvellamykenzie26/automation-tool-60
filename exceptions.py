import time
import functools
import logging

# Logger configured for automation-tool-60
logger = logging.getLogger(__name__)

def retry_on_failure(max_retries=3, delay=2, exceptions=(Exception,)):
    """Decorator to implement exponential backoff retry logic."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay * (2 ** attempt))
            
            logger.error(f"Final attempt failed after {max_retries} retries.")
            raise last_exception
        return wrapper
    return decorator

class NetworkTimeoutError(Exception):
    """Raised when the network operation times out."""
    pass

class ConnectionRefusedError(Exception):
    """Raised when the connection is actively refused."""
    pass