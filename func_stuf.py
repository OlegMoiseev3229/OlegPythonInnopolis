from __future__ import annotations
import time
from functools import lru_cache


def example_function():
    raise Exception("Stub!")


def square(n):
    return n**2


def sum_strings(*args: str):
    return "".join(args)


def sum_strings2(*args: str):
    result = ""
    for s in args:
        result += s
    return result


def append_to_list(s: str, a: list):
    a.append(s.upper())


def fibonacci(n: int, fibs=None):
    """Returns the n-th fibonacci number
    fibonacci(0) = 0
    fibonacci(1) = 1
    fibonacci(n) = fibonacci(n - 2) + fibonacci(n - 1)"""
    if fibs is None:
        fibs = []
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n < len(fibs):
        return fibs[n]
    result = fibonacci(n - 2, fibs=fibs) + fibonacci(n - 1, fibs=fibs)
    fibs.append(result)
    return result


def cache(c: dict | callable = None):
    cache_dict = {}

    def decorator(func):
        def wrapper(*args):
            n = args[0]
            if cache_dict.get(n, None) is None:
                result = func(*args)
                cache_dict[n] = result
                return result
            else:
                return cache_dict[n]
        return wrapper

    if isinstance(c, dict):
        cache_dict = c
        return decorator
    elif callable(c):
        return decorator(c)


def keep_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Running the function {func.__name__} took {t2 - t1} seconds")
        return result
    return wrapper


@cache
def fib(n):
    """Returns the n-th fibonacci number
    fibonacci(0) = 0
    fibonacci(1) = 1
    fibonacci(n) = fibonacci(n - 2) + fibonacci(n - 1)"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    result = fib(n - 2) + fib(n - 1)
    return result


def search_for_69(n):
    return str(n).find("69")


@keep_time
def search_in_fibs():
    for i in range(1000):
        print(search_for_69(fibonacci(i)))


if __name__ == '__main__':
    pass