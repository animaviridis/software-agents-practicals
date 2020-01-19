"""Shapley value calculator."""

import itertools as it


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

    ag = range(1, N+1)

    v = dict()

    for i in ag:
        for co in it.combinations(ag, i):
            print(co)


