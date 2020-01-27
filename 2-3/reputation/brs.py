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


class BRSOpinion(tuple):
    def __new__(cls, r, s, *args, **kwargs):
        return super().__new__(BRSOpinion, BRSOpinion.calculate_opinion(r, s))

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __mul__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError("Argument is not a BRSOpinion object")

        return self.discount_belief(self, other)

    @staticmethod
    def calculate_opinion(r, s):
        den = r + s + 2  # denominator

        b = r / den  # belief?
        d = s / den  # ?
        u = 2 / den  # uncertainty?

        return b, d, u

    @staticmethod
    def discount_belief(xy, yz):
        b_xy, d_xy, u_xy = xy
        b_yz, d_yz, u_yz = yz

        b = b_xy * b_yz
        d = b_xy * d_yz
        u = d_xy + u_xy + b_xy * u_yz

        return b, d, u


# TODO: forgetting


if __name__ == '__main__':
    print(brs_expected(10, 10))
    print(brs_rating(10, 10), '\n')

    print(brs_rating(20, 10))
    print(brs_rating(20, 10, False))

    brs_xy = BRSOpinion(5, 1)
    brs_yz = BRSOpinion(4, 1)

    print("XY b, d, u: ", brs_xy)
    print("YZ b, d, u: ", brs_yz)
    print("XZ b, d, u: ", brs_xy * brs_yz)
