import time
from functools import wraps


def retry(exceptions=Exception, tries=-1, delay=0, backoff=1):
    """
    From https://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/

    Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exceptions: the exception to check. may be a tuple of
        exceptions to check
    :type exceptions: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    """
    def decorator_retry(func):

        @wraps(func)
        def function_retry(*args, **kwargs):
            current_tries, current_delay = tries, delay
            while current_tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    time.sleep(current_delay)
                    current_tries -= 1
                    current_delay *= backoff
            return func(*args, **kwargs)

        return function_retry  # true decorator

    return decorator_retry
