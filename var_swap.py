def swap(a, b):
    a, b = b, a
    print(a, b)


def swap2(a, b):
    t = a
    a = b
    b = t
    print(a, b)


if __name__ == '__main__':
    swap(1, 2)
    swap([1], [2])
    swap2(1, 2)
    swap2([1], [2])
