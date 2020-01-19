"""Shapley value calculator."""

import itertools as it
from math import factorial

def validate(message, t=float):
    val = 0

    while True:
        val_str = input(message)
        if not val_str:
            continue

        try:
            val = t(val_str)
        except ValueError:
            print(f'Invalid input: {val} for conversion to {t}')
        else:
            break

    return val


if __name__ == '__main__':
    N = validate("Enter number of agents: ", int)

    FN = factorial(N)

    ag = range(1, N+1)

    v = {(): 0}

    for i in ag:
        for co in it.combinations(ag, i):
            v[co] = validate(f"Enter value for coalition {co}: ")

    print(v)

    shap = {i: 0 for i in ag}

    for p in it.permutations(ag):
        tail = p[:]
        while len(tail) > 0:
            shap[tail[0]] += (v[tuple(set(tail))] - v[tuple(set(tail[1:]))]) / FN
            tail = tail[1:]

    print(f"\nShapley values: {shap}")
