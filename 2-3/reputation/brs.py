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

        return BRSOpinion(*BRSOpinion.decode_bdu(b, d, u))

    def __add__(self, other):
        if not isinstance(other, BRSOpinion):
            raise TypeError("Not a BRSOpinion object")

        r = self.r + other.r
        s = self.s + other.s
        return BRSOpinion(r, s)

    def expected(self, *args, **kwargs):
        return brs_expected(self.r, self.s, *args, **kwargs)

    @staticmethod
    def decode_bdu(b, d, u):
        return 2*b/u, 2*d/u

    def decode(self):
        return self.decode_bdu(*self)

# TODO: forgetting


if __name__ == '__main__':
    print(brs_expected(10, 10))
    print(brs_rating(10, 10), '\n')

    print(brs_rating(20, 10))
    print(brs_rating(20, 10, False))

    brs_ab = BRSOpinion(5, 2)
    brs_ac = BRSOpinion(1, 0)
    brs_ad = BRSOpinion(4, 3)

    brs_cb = BRSOpinion(6, 2)
    brs_db = BRSOpinion(1, 0)

    print("AB b, d, u: ", brs_ab)
    print("AC b, d, u: ", brs_ac)
    print("AD b, d, u: ", brs_ad)

    print()
    print("ACB b, d, u: ", brs_ac * brs_cb)
    print("ADB b, d, u: ", brs_ad * brs_db)

    brs_acb = brs_ac * brs_cb
    brs_adb = brs_ad * brs_db
    brs_ = brs_acb + brs_adb

    print(f"\nExpected value: A of B based on C and D: {brs_.expected(False)}")
