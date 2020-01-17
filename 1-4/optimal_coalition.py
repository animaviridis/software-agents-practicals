"""Identify the optimal coalition structure, that is, identify what
agents should be allocated to which coalition to maximise the sum of utility. The simplest
way to compute this involves computing the sum of utilities for every possible combination
of coalitions, and picking the highest one.

Implement a simple algorithm to compute the optimal coalition structure.
Your algorithm should simply generate all possible partitions and compute their value, finally
returning the maximal one. Keep track of the time taken to run for 1,2, . . . agents. At
what point does the algorithm start to take too long to run? """


import numpy as np


def generate_utilities(n):
    return dict(zip(range(1, n + 1), np.random.randint(1, 100, n)))


if __name__ == '__main__':
    N = 2  # number of agents
    utilities = generate_utilities(N)
    print(f"{N} agents with utilities: {utilities}")

