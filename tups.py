import time


def test():
    t1 = time.time()

    for _ in range(1_000_000_00):
        a = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        b = sum(a)

    print(t1 - time.time())

    t1 = time.time()
    for _ in range(1_000_000_00):
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        b = sum(a)

    print(t1 - time.time())


if __name__ == '__main__':
    test()