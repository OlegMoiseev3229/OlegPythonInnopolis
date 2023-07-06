import time


class UpperTuple(tuple):
    def __new__(cls, *args, **kwargs):
        new_args = map(str.upper, args)
        return super(UpperTuple, cls).__new__(cls, new_args)


def keep_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Running the function {func.__name__} took {t2 - t1} seconds")
        return result

    return wrapper


@keep_time
def test_tuple():
    for i in range(1_000_000):
        _ = ("gkgjkg", "gkjgkjgaaa", "blb", "gkgjkg", "gkjgkjgaaa", "blb", "gkgjkg", "gkjgkjgaaa", "blb", "gkgjkg",
             "gkjgkjgaaa", "blb", "gkgjkg", "gkjgkjgaaa", "blb")


@keep_time
def test_upper():
    for i in range(1_000_000):
        _ = UpperTuple("gkgjkg", "gkjgkjgaaa", "blb", "gkgjkg", "gkjgkjgaaa", "blb", "gkgjkg", "gkjgkjgaaa", "blb",
                       "gkgjkg",
                       "gkjgkjgaaa", "blb", "gkgjkg", "gkjgkjgaaa", "blb")


def main():
    print(UpperTuple("bla", "alb", "blb"))


if __name__ == '__main__':
    main()
