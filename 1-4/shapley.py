"""Shapley value calculator."""

import itertools as it
from math import factorial

from misc import misc


def ask_utilities(agents):
    ut = {(): 0}

    for i in agents:
        for co in it.combinations(ag, i):
            ut[co] = misc.validate(f"Enter value for coalition {co}: ")

    return ut


def compute_shapley(ut):
    shap = {i: 0 for i in ag}

    for p in it.permutations(ag):
        tail = p[:]
        while len(tail) > 0:
            shap[tail[0]] += (ut[tuple(set(tail))] - ut[tuple(set(tail[1:]))]) / FN
            tail = tail[1:]

    return shap


if __name__ == '__main__':
    N = misc.validate("Enter number of agents: ", int)

    FN = factorial(N)

    ag = range(1, N+1)
    v = ask_utilities(ag)
    print(v)

    shap = compute_shapley(v)

    print(f"\nShapley values: {shap}")
