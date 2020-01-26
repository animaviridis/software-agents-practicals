# Beta-reputation system


def smoothing(func):
    def wrapper(a, b, smooth=True):
        if smooth:
            a += 1
            b += 1

        return func(a, b)
    return wrapper


@smoothing
def brs_expected(a, b):
    return a / (a + b)


@smoothing
def brs_rating(a, b):
    return (a - b) / (a + b + 2)


if __name__ == '__main__':
    print(brs_expected(10, 10))
    print(brs_rating(10, 10), '\n')

    print(brs_rating(20, 10))
    print(brs_rating(20, 10, False))
