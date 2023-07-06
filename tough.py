import time


def area_calculation(shape):
    def rect_area(a, b):
        return a*b

    def circle_area(r):
        return 3.14159 * r * r

    def square_area(a):
        return a * a

    def triangle_area(base, height):
        return base * height * 1/2

    if shape == "rectangle":
        return rect_area
    elif shape == "circle":
        return circle_area
    elif shape == "square":
        return square_area
    elif shape == "triangle":
        return triangle_area


def repeat(n):
    def wrapper(func):
        def r(*args, **kwargs):
            for i in range(n):
                func(*args, **kwargs)
        return r
    return wrapper


def compose(*funcs):
    funcs = reversed(funcs)

    def iterate(*args, **kwargs):
        for foo in funcs:
            foo(*args, **kwargs)

    return iterate


@repeat(5)
def print_upper(text, **kwargs):
    print(text.upper(), **kwargs)


def keep_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Running the function {func.__name__} took {t2 - t1} seconds")
        return result
    return wrapper


if __name__ == '__main__':
    print_upper("agjhgbhabgjhagkjgh")
