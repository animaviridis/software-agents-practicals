"""Shapley value from MC-nets including negative literals """


from math import factorial


def shap_pos(v, p, n):
    if n == 0:
        return v/p

    return v * factorial(p-1) * factorial(n) / factorial(p+n)


def shap_neg(v, p, n):
    return (- v) * factorial(p) * factorial(n - 1) / factorial(p+n)
