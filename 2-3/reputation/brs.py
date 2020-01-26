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


@smoothing
def brs_opinion(r, s):
    den = r + s + 2  # denominator

    b = r / den  # belief?
    d = s / den  # ?
    u = 2 / den  # uncertainty?

    return b, d, u


def discount_belief(xy, yz):
    b_xy, d_xy, u_xy = xy
    b_yz, d_yz, u_yz = yz

    b = b_xy * b_yz
    d = b_xy * d_yz
    u = d_xy + u_xy + b_xy * u_yz

    return b, d, u


if __name__ == '__main__':
    print(brs_expected(10, 10))
    print(brs_rating(10, 10), '\n')

    print(brs_rating(20, 10))
    print(brs_rating(20, 10, False))

    print("\nb, d, u: ", brs_opinion(10, 20))

    print('\nDiscounting beliefs:', discount_belief(brs_opinion(10, 20), brs_opinion(30, 2)))
